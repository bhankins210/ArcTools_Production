# import pre-geocoded locations table and add to TOC
import arcpy
import msparkdb	

# define map document and dataframe
mxd = arcpy.mapping.MapDocument(r"CURRENT")
df = arcpy.mapping.ListDataFrames(mxd,'*')[0]

# input parameters
request_in = arcpy.GetParameterAsText(0)
request_id = request_in.upper() 
loc_name = arcpy.GetParameterAsText(1)
loc_in = loc_name + '\SHEET1$'
new_db = arcpy.GetParameterAsText(2)
new_mdb_loc = arcpy.GetParameterAsText(3)
new_mdb_name = arcpy.GetParameterAsText(4)
mdb_loc = arcpy.GetParameterAsText(5)

# define variables
loc_out = request_id + "_LOC"
loc_table = request_id + '_loc_table'
xy_event = request_id + '_xy_event'

# define database		
if str(new_db) == 'true':
	space = msparkdb.newmdb(new_mdb_loc,new_mdb_name)
else: 
	space = mdb_loc

# create location table
arcpy.env.workspace = space
msparkdb.loctable(loc_in,space,loc_table,xy_event)
		

