import arcpy
import msparkdb


#Define variable through ArcMap script
request_in = arcpy.GetParameterAsText(0)
request_id = request_in.upper() 
loc_out = request_id + '_LOC'
address_in = arcpy.GetParameterAsText(1)
city_in = arcpy.GetParameterAsText(2)
state_in = arcpy.GetParameterAsText(3)
zip_in = arcpy.GetParameter(4)
store_in = arcpy.GetParameterAsText(5)

# create new database
new_db = arcpy.GetParameterAsText(6)
new_mdb_loc = arcpy.GetParameterAsText(7)
new_mdb_name = arcpy.GetParameterAsText(8)

# use existing database
mdb_loc = arcpy.GetParameterAsText(9)

# define database		
if str(new_db) == 'true':
	space = msparkdb.newmdb(new_mdb_loc,new_mdb_name)
else: 
	space = mdb_loc
arcpy.env.workspace = space

# create temp table and load address from import
msparkdb.temploctable(request_id,address_in, city_in, state_in, zip_in, store_in)

# geocode single location		
msparkdb.geocode(request_id,loc_out)

# add geocoded location to TOC
msparkdb.loadlayer(loc_out)

# clean location table
msparkdb.cleanloctable(loc_out)

# refresh views
arcpy.RefreshTOC()
arcpy.RefreshActiveView()

