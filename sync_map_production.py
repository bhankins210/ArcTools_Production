import arcpy
import msparkdb

#define input parameters
view_name_in = arcpy.GetParameterAsText(0)

# reset selected to 0
msparkdb.syncmapupdate(view_name_in)

# execute sync map to grid
msparkdb.syncmaprun(view_name_in)

# Delete table records if "selected" = 0
msparkdb.syncmapdelete(view_name_in)

# refresh view and clear selected feature		
msparkdb.clearlayer(view_name_in)
		

