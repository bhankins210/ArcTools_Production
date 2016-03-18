import arcpy
import msparkdb

#define input parameters
view_name_in = arcpy.GetParameterAsText(0)

# remove distance profile, store, and reset view to original state
msparkdb.resetview(view_name_in)




