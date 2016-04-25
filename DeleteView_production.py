import arcpy
import msparkdb

#define input parameters
view_name_in = arcpy.GetParameterAsText(0)

# delete spatial view
msparkdb.deleteview(view_name_in)

# refresh catalog view
db_connection = r'Database Connections\arc_spatial_view.sde'	
arcpy.RefreshCatalog(db_connection)	






