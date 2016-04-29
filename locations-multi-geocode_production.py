import arcpy
import msparkdb

#define script parameters
request_in = arcpy.GetParameterAsText(0)
request_id = request_in.upper() 
loc_name = arcpy.GetParameterAsText(1)
loc_in = loc_name + '\SHEET1$'
loc_out = request_id + "_LOC"
loc_table = request_id + '_loc_table'

# create new database
new_db = arcpy.GetParameterAsText(2)
new_mdb_loc = arcpy.GetParameterAsText(3)
new_mdb_name = arcpy.GetParameterAsText(4)

# use existing mdb
mdb_loc = arcpy.GetParameterAsText(5)

# define database		
if str(new_db) == 'true':
	space = msparkdb.newmdb(new_mdb_loc,new_mdb_name)
else: 
	space = mdb_loc
arcpy.env.workspace = space

#create location table
msparkdb.multiloctemp(loc_in,loc_table)

#Geocode location
msparkdb.geocodemulti(loc_table,loc_out)

# add geocoded location to TOC
msparkdb.loadlayer(loc_out)

# clean location table
msparkdb.cleanloctable(loc_out)

# refresh views
arcpy.RefreshTOC()
arcpy.RefreshActiveView()

