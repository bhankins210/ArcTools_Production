import arcpy
import time  
import msparkdb

#define input parameters
# spatial view prefix
table_name_in = arcpy.GetParameterAsText(0)
table_name = table_name_in.upper()

# define level(s) of geography to create views for:
zip = arcpy.GetParameterAsText(1)
split = arcpy.GetParameterAsText(2)
route = arcpy.GetParameterAsText(3)

# run clean spatial view stored procedure.  
clean_view = arcpy.GetParameterAsText(4)

# specify start and end date to create spatial views for:
start_date_in = arcpy.GetParameterAsText(5)
end_date_in = arcpy.GetParameterAsText(6)
start_date = str(start_date_in)
end_date = str(end_date_in)

# determine which states to create spatial views for.
state_string = arcpy.GetParameterAsText(7)
all_state = arcpy.GetParameterAsText(8)

# auto add created layers to TOC.  Default False
auto_add = arcpy.GetParameterAsText(9)

# convert state_string to comma separated string list
if str(all_state) == 'true':
	state_parameter = '()'
if str(all_state) == 'false':
	state_parameter = msparkdb.stateconvert(state_string)
	
# Create zip spatial view
if str(zip) == 'true':	
	zip_table = 'tblz_' + table_name
	zip_view = 'svwz_' + table_name
	zip_layer = 'svwz_' + table_name
	msparkdb.spatialview(zip_table, start_date, end_date, zip_view, state_parameter)

# Create split spatial view
if str(split) == 'true':	
	split_table = 'tbls_' + table_name
	split_view = 'svws_' + table_name
	split_layer = 'svws_' + table_name
	msparkdb.spatialview(split_table, start_date, end_date, split_view, state_parameter)	

# Create route spatial view
if str(route) == 'true':	
	route_table = 'tblr_' + table_name
	route_view = 'svwr_' + table_name
	route_layer = 'svwr_' + table_name
	msparkdb.spatialview(route_table, start_date, end_date, route_view, state_parameter)	
		
# clean views
if str(clean_view) == 'true':
	if str(zip) == 'true':	
		msparkdb.cleanview(zip_table)
	if str(split) == 'true':
		msparkdb.cleanview(split_table)
	if str(route) == 'true':
		msparkdb.cleanview(route_table)

# add view layers to TOC	
db_connection = 'Database Connections\spatial_view.sde'	
arcpy.RefreshCatalog(db_connection)	

if str(auto_add) == 'true':
# if add_layers == 'yes':
	if str(zip) == 'true':
		msparkdb.importview(zip_view)
	if str(split) == 'true':
		msparkdb.importview(split_view)
	if str(route) == 'true':
		msparkdb.importview(route_view)
	
	arcpy.RefreshTOC()
	arcpy.RefreshActiveView()
	