
python calculate_groundwater_footprint.py "/scratch-shared/edwinhs/groundwater_foot_print_july_2017/groundwater_stress_1990-2014/state/" state 1990 1991 &
python calculate_groundwater_footprint.py "/scratch-shared/edwinhs/groundwater_foot_print_july_2017/groundwater_stress_1990-2014/pixel/" pixel 1990 1991 &
wait
python calculate_groundwater_footprint.py "/scratch-shared/edwinhs/groundwater_foot_print_july_2017/groundwater_stress_1990-2014/aquifer/" aquifer 1990 1991 &
python calculate_groundwater_footprint.py "/scratch-shared/edwinhs/groundwater_foot_print_july_2017/groundwater_stress_1990-2014/drainage_unit/" drainage_unit 1990 1991 &
wait

