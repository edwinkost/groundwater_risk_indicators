#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pcraster as pcr
import calendar
import datetime

import virtualOS as vos

# reporting module
import output_netcdf_cf_convention as outputNetCDF

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
#~ class_map_default_folder = "/projects/0/dfguu/users/edwin/data/aqueduct_gis_layers/aqueduct_shp_from_marta/" 
class_map_default_folder = "/projects/0/dfguu/users/edwin/data/aqueduct_gis_layers/aqueduct_raster_units_version_july_2017/spatial_units/"
if class_map_file_name == "state": class_map_file_name = class_map_default_folder + "/Aqueduct_States.map"
if class_map_file_name == "drainage": class_map_file_name = class_map_default_folder + "/hybas_merged_custom_level6_V01.map"             # Aqueduct_GDBD.map
if class_map_file_name == "aquifer": class_map_file_name = class_map_default_folder + "/whymap_wgs1984_BUENO.map"                             # why_wgs1984_BUENO.map
if class_map_file_name == "country": class_map_file_name = "/projects/0/dfguu/users/edwin/data/country_shp_from_tianyi/World_Polys_High.map"

# reading the class map
class_map    = pcr.nominal(pcr.uniqueid(landmask))
if class_map_file_name != "pixel":
	class_map = vos.readPCRmapClone(class_map_file_name, clone_map, tmp_directory, None, False, None, True, False)
	class_map = pcr.ifthen(pcr.scalar(class_map) > 0.0, pcr.nominal(class_map)) 

# limit the class to the landmask only:
class_map     = pcr.ifthen(landmask, class_map)

# time selection
start_year = int(sys.argv[3])
end_year   = int(sys.argv[4])
 
# text/string for the spatial unit
text_unit = str(sys.argv[2])
if text_unit == "pixel": text_unit = "5 arc-minute resolution"
if text_unit == "state": text_unit = "GADM states"
if text_unit == "drainage": text_unit = "HydroBasin Level 6"
if text_unit == "aquifer": text_unit = "WHYMAP aquifers"

# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']          = "NETCDF4"
netcdf_setup['zlib']            = False
netcdf_setup['institution']     = "Department of Physical Geography, Utrecht University ; Deltares ; World Resources Institute"
netcdf_setup['title'      ]     = "PCR-GLOBWB-MODFLOW (offline coupled) output: Monthly groundwater head changes at the spatial unit of " + text_unit 
netcdf_setup['created by' ]     = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl) ; Sandra Galvis Rodriguez (Sandra.GalvisRodriguez@deltares.nl) ; Marta Faneca Sanchez [Marta.FanecaSanchez@deltares.nl]"
netcdf_setup['description']     = "Monthly groundwater head changes at the spatial unit/level of " + text_unit + ", calculated based on the 5 arc-minute simulation result of the offline coupled simulation of the PCR-GLOBWB-MODFLOW model forced with the forcing data of CRU downscaled with ERA-40 and ERA-Interim"
netcdf_setup['source'     ]     = "Utrecht University, Department of Physical Geography - contact: Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['references' ]     = ""
netcdf_setup['references' ]    += "Sutanudjaja, E.H., van Beek, R., Wada, Y., Bosmans, J., Drost, N., de Graaf, I., de Jong, K., Lopez Lopez, P., Pessenteiner, S., Oliver, S., Straatsma, M., Wanders, N., Wisser, D., and Bierkens, M.F.P.: PCR-GLOBWB 2.0: a 5 arc-minute global hydrological and water resources model, to be submitted to Geosci. Model Dev. Discuss., in preparation, 2017. "
netcdf_setup['references' ]    += "Sutanudjaja, E.H., van Beek, R., Wada, Y., Bosmans, J., Drost, N., de Graaf, I., de Jong, K., Lopez Lopez, P., Pessenteiner, S., Oliver, S., Straatsma, M., Wanders, N., Wisser, D., and Bierkens, M.F.P.: PCR-GLOBWB_model, available at: https://github.com/UU-Hydro/PCR-GLOBWB_model, 2017. "
netcdf_setup['references' ]    += "de Graaf, I.E.M., van Beek, R., Gleeson, T., Moosdorf, N., Schmitz, O., Sutanudjaja, E.H., Bierkens, M.F.P.: A global-scale two-layer transient groundwater model: Development and application to groundwater depletion, Adv. Water Resour., 102, 53–67, doi:10.1016/j.advwatres.2017.01.011, 2017. "
netcdf_setup['references' ]    += "Faneca Sanchez, M., Sutanudjaja, E.H., Kuijper M., and Bierkens, M.F.P.: Global Groundwater related Risk Indicators: quantifying groundwater stress and groundwater table decline (1990-2010) at global scale, EGU General Assembly, 2016. "
netcdf_setup['references' ]    += "Erkens, G. and Sutanudjaja, E. H.: Towards a global land subsidence map, Proc. IAHS, 372, 83-87, https://doi.org/10.5194/piahs-372-83-2015, 2015. "
netcdf_setup['references' ]    += "de Graaf, I. E. M., Sutanudjaja, E. H., van Beek, L. P. H., and Bierkens, M. F. P.: A high-resolution global-scale groundwater model, Hydrol. Earth Syst. Sci., 19, 823-837, https://doi.org/10.5194/hess-19-823-2015, 2015. "
netcdf_setup['references' ]    += "Sutanudjaja, E. H., van Beek, L. P. H., de Jong, S. M., van Geer, F. C., and Bierkens, M. F. P.: Calibrating a large-extent high resolution coupled groundwater-land surface model using soil moisture and discharge data, Water Resour. Res., 50, 687–705, doi:10.1002/2013WR013807, 2014."
netcdf_setup['references' ]    += "van Beek, R., Wada, Y., and Bierkens, M. F. P.: Global monthly water stress: 1. Water balance and water availability, Water Resour. Res., 47, W07517, doi:10.1029/2010WR009791, 2011. "
netcdf_setup['references' ]    += "Sutanudjaja, E. H., van Beek, L. P. H., de Jong, S. M., van Geer, F. C., and Bierkens, M. F. P.: Large-scale groundwater modeling using global datasets: a test case for the Rhine-Meuse basin, Hydrol. Earth Syst. Sci., 15, 2913–2935, doi:10.5194/hess-15-2913-2011, 2011."



# references for the spatial unit:
spatial_unit_reference = ""
if class_map_file_name == "aquifer": spatial_unit_reference = "BGR/UNESCO: Groundwater Resources of the World 1: 25 000 000, http://www.whymap.org/whymap/EN/Products/products_node_en.html, 2008."
if class_map_file_name == "state": spatial_unit_reference = "Global Administrative Areas: GADM database of Global Administrative Areas, http://www.gadm.org/home, 2015. "
if class_map_file_name == "drainage": "Lehner, B., Grill, G.: Global river hydrography and network routing: baseline data and new approaches to study the world’s large river systems. Hydrological Processes, 27(15): 2171–2186, data is available at http://hydrosheds.org, 2013. "
netcdf_setup['references' ]    += spatial_unit_reference 


# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()

msg = "Preparing netcdf output files (following the aqueduct convention)."
print(msg)
#
#
# - the dictionary for attribute information for netcdf files
netcdf_file = {}
# - variable name
var_name = 'groundwater_head_changes' 
netcdf_file[var_name] = {}
#
# - resolution (unit: arc-minutes)
netcdf_file[var_name]['resolution_arcmin'] = 5.0 
#
# - general attribute information:
netcdf_file[var_name]['description'] = netcdf_setup['description']
netcdf_file[var_name]['institution'] = netcdf_setup['institution']
netcdf_file[var_name]['title'      ] = netcdf_setup['title'      ]
netcdf_file[var_name]['created by' ] = netcdf_setup['created by' ]
netcdf_file[var_name]['source'     ] = netcdf_setup['source'     ]
netcdf_file[var_name]['references' ] = netcdf_setup['references' ]


# - preparing netcdf file:
output_netcdf_file_name = output_directory + "/" + str(sys.argv[2]) + "_" + str(start_year) + "to" + str(end_year) + ".monthly_groundwater_head_changes.nc"
msg = "Preparing the netcdf file: " + output_netcdf_file_name
print(msg)
netcdf_file[var_name]['file_name'] = output_netcdf_file_name
netcdf_report.create_netcdf_file(netcdf_file[var_name]) 
#
# - creating variable for the class/spatial units
netcdf_report.create_variable(\
                              ncFileName = output_netcdf_file_name, \
                              varName    = "spatial_unit", \
                              varUnit    = "-", \
                              longName   = str(sys.argv[2]) + "_spatial_unit", \
                              comment    = "The spatial unit is based on " + text_unit + "."
                              )
#
# annual_rate_of_groundwater_head_decline
# - variable name, unit, comment, etc. 
variable_name = var_name
var_long_name = "monthly_groundwater_head_changes"
variable_unit = "m.month-1"
var_comment   = "Monthly groundwater head changes. Positive values indicate that groundwater heads are higher then their previous values."
# - creating variable 
netcdf_report.create_variable(\
                              ncFileName = output_netcdf_file_name, \
                              varName    = variable_name, \
                              varUnit    = variable_unit, \
                              longName   = var_long_name, \
                              comment    = var_comment
                              )

# netcdf input file:
if str(sys.argv[2]) == "state":    head_difference_file_name = "/scratch/shared/edwinhs/data_from_sandra/GW_Differences_Relative_1990/GW_Head_Difference_States.nc"
if str(sys.argv[2]) == "drainage": head_difference_file_name = "/scratch/shared/edwinhs/data_from_sandra/GW_Differences_Relative_1990/GW_Head_Difference_hybas6.nc"
if str(sys.argv[2]) == "aquifer":  head_difference_file_name = "/scratch/shared/edwinhs/data_from_sandra/GW_Differences_Relative_1990/GW_Head_Difference_aquifer.nc"
if str(sys.argv[2]) == "pixel":    head_difference_file_name = "/scratch/shared/edwinhs/data_from_sandra/GW_Differences_Relative_1990/GW_Head_Difference_pixel.nc"


# write variables to netcdf files
# - index for the necdf input file
i_time = 0
 
for year in range(start_year, end_year, 1):
    #
    end_month = 12
    if year == end_year: end_month = 11
    #
    for month in range(1, end_month + 1, 1):
        #
        # - time bounds for netcdf files
        if month < 12:
            lowerTimeBound = datetime.datetime(  year, month    , 15, 0)
            upperTimeBound = datetime.datetime(  year, month + 1, 15, 0)
        else:
            lowerTimeBound = datetime.datetime(  year    , month, 15, 0)
            upperTimeBound = datetime.datetime(  year + 1, 1    , 15, 0)
        timeBounds = [lowerTimeBound, upperTimeBound]
        #
        # - spatial unit
        spatial_unit = pcr.ifthen(landmask, class_map)
        netcdf_report.data_to_netcdf(output_netcdf_file_name, "spatial_unit", pcr.pcr2numpy(pcr.scalar(spatial_unit) , vos.MV), timeBounds, timeStamp = None, posCnt = i_time)
        #
        # - groundwater_head_difference_values
        head_difference = vos.netcdf2PCRobjClone(head_difference_file_name, "groundwater_head_dif", i_time - 1, "Yes")
        head_difference = pcr.ifthen(landmask, head_difference)
        head_difference = pcr.areamaximum(head_difference, spatial_unit)
        netcdf_report.data_to_netcdf(output_netcdf_file_name, "groundwater_head_changes", pcr.pcr2numpy(head_difference, vos.MV), timeBounds, timeStamp = None, posCnt = i_time)
        #
        # updating time index
        i_time = i_time + 1
