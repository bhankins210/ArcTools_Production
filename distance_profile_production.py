import arcpy
import msparkdb

# location table - after geocoding
loc_table_in = arcpy.GetParameterAsText(0)

# spatial view to profile
view_name_in = arcpy.GetParameterAsText(1)

# Maximum Distance
max_radius = arcpy.GetParameterAsText(2)

# Handle duplication
dupl = arcpy.GetParameterAsText(3)

# execute profile stored procedures
msparkdb.profileloc(loc_table_in,view_name_in,max_radius)
if str(dupl) == 'true':
	msparkdb.duplprofileloc(loc_table_in,view_name_in,max_radius)


