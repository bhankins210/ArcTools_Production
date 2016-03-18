import arcpy
import msparkdb

#define input parameters
view_name_in = arcpy.GetParameterAsText(0)

# delete spatial view
msparkdb.deleteview(view_name_in)



