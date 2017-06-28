#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pcraster as pcr
import calendar

import virtualOS as vos

# output directory
output_directory = os.path.dirname(str(sys.argv[1]))
try:
	os.makedirs(output_directory)
except:
	pass

# making temporary directory:
tmp_directory = output_directory + "/tmp/"
try:
	os.makedirs(tmp_directory)
except:
	pass

# set clone
clone_map = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(clone_map)

# landmask map
landmask = pcr.defined(pcr.readmap(clone_map))

# class map file name:
#~ class_map_file_name = "/projects/0/dfguu/users/edwin/data/aqueduct_gis_layers/aqueduct_shp_from_marta/Aqueduct_States.map"
#~ class_map_file_name = "/projects/0/dfguu/users/edwin/data/aqueduct_gis_layers/aqueduct_shp_from_marta/Aqueduct_GDBD.map"
#~ class_map_file_name = "/projects/0/dfguu/users/edwin/data/processing_whymap/version_19september2014/major_aquifer_30min.extended.map"
#~ class_map_file_name = "/projects/0/dfguu/users/edwin/data/processing_whymap/version_19september2014/major_aquifer_30min.map"
class_map_file_name = str(sys.argv[2])
class_map_default_folder = "/projects/0/dfguu/users/edwin/data/aqueduct_gis_layers/aqueduct_shp_from_marta/" 
if class_map_file_name == "state": class_map_file_name = class_map_default_folder + "/Aqueduct_States.map"
if class_map_file_name == "drainage_unit": class_map_file_name = class_map_default_folder + "/Aqueduct_GDBD.map"
if class_map_file_name == "aquifer": class_map_file_name = class_map_default_folder + "/why_wgs1984_BUENO.map"
if class_map_file_name == "country": class_map_file_name = "/projects/0/dfguu/users/edwin/data/country_shp_from_tianyi/World_Polys_High.map"

# reading the class map
class_map    = pcr.nominal(pcr.uniqueid(landmask))
if class_map_file_name != "pixel":
	class_map = vos.readPCRmapClone(class_map_file_name, clone_map, tmp_directory, None, False, None, True, False)
	class_map = pcr.ifthen(pcr.scalar(class_map) > 0.0, pcr.nominal(class_map)) 

# time selection
start_year = int(sys.argv[3])
end_year   = int(sys.argv[4])
 
# cell_area (unit: m2)
cell_area = pcr.readmap("/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map") 
segment_cell_area = pcr.areatotal(cell_area, class_map)

# extent of aquifer/sedimentary basins:
#~ sedimentary_basin = pcr.cover(pcr.scalar(pcr.readmap("/projects/0/dfguu/users/edwin/data/sed_extent/sed_extent.map")), 0.0)
#~ cell_area = sedimentary_basin * cell_area
#~ cell_area = pcr.ifthenelse(pcr.areatotal(cell_area, class_map) > 0.25 * segment_cell_area, cell_area, 0.0)

class_map_all = class_map
#~ # we only use pixels belonging to the sedimentary basin
#~ class_map     = pcr.ifthen(sedimentary_basin > 0, class_map)

# fraction for groundwater recharge to be reserved to meet the environmental flow
fraction_reserved_recharge = pcr.readmap("/scratch-shared/edwinsut/fraction_reserved_recharge_rens/reservedrecharge/fraction_reserved_recharge10.5min.map")
# - extrapolation
fraction_reserved_recharge = pcr.cover(fraction_reserved_recharge, \
                                       pcr.windowaverage(fraction_reserved_recharge, 0.5))
fraction_reserved_recharge = pcr.cover(fraction_reserved_recharge, \
                                       pcr.windowaverage(fraction_reserved_recharge, 0.5))
fraction_reserved_recharge = pcr.cover(fraction_reserved_recharge, \
                                       pcr.windowaverage(fraction_reserved_recharge, 0.5))
fraction_reserved_recharge = pcr.cover(fraction_reserved_recharge, \
                                       pcr.windowaverage(fraction_reserved_recharge, 0.5))
fraction_reserved_recharge = pcr.cover(fraction_reserved_recharge, \
                                       pcr.windowaverage(fraction_reserved_recharge, 0.5))
fraction_reserved_recharge = pcr.cover(fraction_reserved_recharge, \
                                       pcr.windowaverage(fraction_reserved_recharge, 0.5))
fraction_reserved_recharge = pcr.cover(fraction_reserved_recharge, \
                                       pcr.windowaverage(fraction_reserved_recharge, 0.5))
fraction_reserved_recharge = pcr.cover(fraction_reserved_recharge, 0.1)
# - set minimum value to 0.30
fraction_reserved_recharge = pcr.max(0.30, fraction_reserved_recharge)
# - set maximum value to 0.30
fraction_reserved_recharge = pcr.min(0.70, fraction_reserved_recharge)

# areal_groundwater_abstraction (unit: m/year)
#~ groundwater_abstraction = pcr.cover(pcr.readmap("/nfsarchive/edwin-emergency-backup-DO-NOT-DELETE/rapid/edwin/05min_runs_results/2015_04_27/non_natural_2015_04_27/global/analysis/avg_values_1990_to_2010/totalGroundwaterAbstraction_annuaTot_output_1990to2010.map"), 0.0)
groundwater_abstraction = pcr.scalar(0.0)
for year in range(start_year, end_year + 1, 1):
    for month in range(1, 12 + 1, 1):
        date_in_string  = str(calendar.monthrange(year, month)[1])
        month_in_string = str(month)
        if month < 10: month_in_string = "0" + month_in_string 
        date_input_in_string = str(year) + "-" + month_in_string + "-" + date_in_string
        netcdf_file   = "/projects/0/aqueduct/users/edwinsut/05min_runs_rerun_for_WRI_version_27_april_2015_with_more_daily_ouputs/merged_1959_to_2015/global/netcdf/totalGroundwaterAbstraction_monthTot_output_1959-01-31_to_2015-12-31.nc"
        variable_name = "total_groundwater_abstraction"
        groundwater_abstraction += pcr.cover(
                                   vos.netcdf2PCRobjClone(ncFile = netcdf_file, varName = variable_name, dateInput = date_input_in_string,\
                                                          useDoy = None,
                                                          cloneMapFileName  = None,\
                                                          LatitudeLongitude = True,\
                                                          specificFillValue = None), 0.0)
# convert to m/year
groundwater_abstraction = groundwater_abstraction / (end_year - start_year + 1)
areal_groundwater_abstraction = pcr.cover(pcr.areatotal(groundwater_abstraction * cell_area, class_map)/pcr.areatotal(cell_area, class_map), 0.0)

# areal groundwater recharge (unit: m/year)
# cdo command: cdo setunit,m.year-1 -timavg -yearsum -selyear,1990/2010 ../../netcdf/gwRecharge_monthTot_output.nc gwRecharge_annuaTot_output_1990to2010.nc
#~ groundwater_recharge = pcr.cover(pcr.readmap("/nfsarchive/edwin-emergency-backup-DO-NOT-DELETE/rapid/edwin/05min_runs_results/2015_04_27/non_natural_2015_04_27/global/analysis/avg_values_1990_to_2010/gwRecharge_annuaTot_output_1990to2010.map"), 0.0) 
groundwater_recharge = pcr.scalar(0.0)
for year in range(start_year, end_year + 1, 1):
    for month in range(1, 12 + 1, 1):
        date_in_string  = str(calendar.monthrange(year, month)[1])
        month_in_string = str(month)
        if month < 10: month_in_string = "0" + month_in_string 
        date_input_in_string = str(year) + "-" + month_in_string + "-" + date_in_string
        netcdf_file   = "/projects/0/aqueduct/users/edwinsut/05min_runs_rerun_for_WRI_version_27_april_2015_with_more_daily_ouputs/merged_1959_to_2015/global/netcdf/gwRecharge_monthTot_output_1958-01-31_to_2015-12-31.nc"
        variable_name = "groundwater_recharge"
        groundwater_recharge += pcr.cover(
                                vos.netcdf2PCRobjClone(ncFile = netcdf_file, varName = variable_name, dateInput = date_input_in_string,\
                                                       useDoy = None,
                                                       cloneMapFileName  = None,\
                                                       LatitudeLongitude = True,\
                                                       specificFillValue = None), 0.0)
# convert to m/year
groundwater_recharge = groundwater_recharge / (end_year - start_year + 1)
areal_groundwater_recharge = pcr.areatotal(groundwater_recharge * cell_area, class_map)/pcr.areatotal(cell_area, class_map)
# - ignore negative groundwater recharge (due to capillary rise)
areal_groundwater_recharge = pcr.max(0.0, areal_groundwater_recharge)

# areal groundwater contribution to meet enviromental flow (unit: m/year)
#~ groundwater_contribution_to_environmental_flow       = pcr.max(0.10, fraction_reserved_recharge * groundwater_recharge)  # THIS IS WRONG.
groundwater_contribution_to_environmental_flow          = fraction_reserved_recharge * groundwater_recharge
groundwater_contribution_to_environmental_flow_filename = output_directory + "/" + "groundwater_contribution_to_environmental_flow.m.per.year.map" 
pcr.report(pcr.ifthen(landmask, groundwater_contribution_to_environmental_flow), groundwater_contribution_to_environmental_flow_filename)
areal_groundwater_contribution_to_environmental_flow = pcr.areatotal(groundwater_contribution_to_environmental_flow * cell_area, class_map)/pcr.areatotal(cell_area, class_map) 
areal_groundwater_contribution_to_environmental_flow = pcr.min(0.75 * areal_groundwater_recharge, areal_groundwater_contribution_to_environmental_flow)

# groundwater stress map (dimensionless)
groundwater_stress_map = pcr.ifthen(landmask, \
                             areal_groundwater_abstraction/(pcr.cover(pcr.max(0.001, areal_groundwater_recharge - areal_groundwater_contribution_to_environmental_flow), 0.001)))
#~ # fill in the entire cell
#~ groundwater_stress_map = pcr.ifthen(landmask, \
                         #~ pcr.areamaximum(groundwater_stress_map, class_map_all))
groundwater_stress_map_filename = output_directory + "/" + str(sys.argv[2]) + "_" + str(start_year) + "to" + str(end_year) + ".groundwater_stress.map"
pcr.report(groundwater_stress_map, groundwater_stress_map_filename)
#~ pcr.aguila(groundwater_stress_map)

# groundwater footprint map (km2)
groundwater_footprint_map = groundwater_stress_map * pcr.cover(pcr.areatotal(cell_area, class_map), 0.0) / (1000. * 1000.)
groundwater_footprint_map_filename = output_directory + "/" + str(sys.argv[2]) + "_" + str(start_year) + "to" + str(end_year) + ".groundwater_footprint.km2.map"
pcr.report(groundwater_footprint_map, groundwater_footprint_map_filename)
#~ pcr.aguila(groundwater_footprint_map)


