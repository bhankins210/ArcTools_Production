import arcpy
import msparkdb

# input parameters
view_name_in = arcpy.GetParameterAsText(0)
sv_query = arcpy.GetParameterAsText(1)

# delete view features based on view
msparkdb.viewquery(view_name_in,sv_query)