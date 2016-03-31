"""
Spatial View Function Module

"""

import arcpy
import pypyodbc


# define working mxd file, data frame, and sde connection
mxd = arcpy.mapping.MapDocument(r"CURRENT")
df = arcpy.mapping.ListDataFrames(mxd,'*')[0]	
db_connection = 'Database Connections\spatial_view.sde'
sr = r"C:\Program Files (x86)\ArcGIS\Desktop10.3\Reference Systems\WGS 1984 Web Mercator (auxiliary sphere).prj"

# # Creates databse connection via pypyodbc
def dbconn():
	try:
		connection = pypyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=mapping-sqldev\esri;DATABASE=spatial_view;UID=id;PWD=pass;Trusted_Connection=Yes')
		return connection
	except:
		print 'Cannot connect to database'


# ***********************************spatial view functions*************************************		
# Runs clean view stored procedure
def cleanview(table_name):
	try:
		con = dbconn()
		cur = con.cursor()
		table_clean = "'" + table_name + "'"
		sql_command = """EXEC [dbo].[gis_clean_view] %s""" % table_clean
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'Clean View Failed'

		
# imports spatial view into current map document		
def importview(view_name):
	try:
		select_query = 'select * from ' + view_name
		sr = 'GEOGCS["GCS_Assumed_Geographic_1",DATUM["D_North_American_1927",SPHEROID["Clarke_1866",6378206.4,294.9786982]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
		srid = '104000'
		arcpy.MakeQueryLayer_management(db_connection,view_name,select_query,"ID","POLYGON",srid,sr)
		layer = arcpy.mapping.Layer(view_name)
		arcpy.mapping.AddLayer(df, layer, "TOP")
	except:
		print 'Could not load view'

		
# convert state input into sql parameter
def stateconvert(state_in):
	try:
		state_string = state_in.upper()
		state_tuple = tuple(state_string.split(','))
		state_parameter = ''
		for state in state_tuple:
			state_parameter = state_parameter + "''" + state + "'',"
		state_parameter = state_parameter[:-1]
		state_parameter = '(' + state_parameter + ')'
		return state_parameter
	except:
		print 'could not convert states'

		
# runs spatial view stored procedure
def spatialview(*in_var):
	try:
		sql_param_tup = in_var
		con = dbconn()
		cur = con.cursor()
		sql_command = """EXEC [dbo].[gis_spatialview_combined] '%s','%s','%s','%s','%s'""" % (sql_param_tup)
		arcpy.AddMessage(sql_command)
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'could not create view'


# delete spatial view
def deleteview(view_name_in):
	try:
		view_space = view_name_in.find('svw')
		view_name = view_name_in[view_space:]
		con = dbconn()
		cur = con.cursor()
		sql_command = """EXEC [dbo].[gis_delete_spatialview] '%s'""" % view_name
		cur.execute(sql_command)
		con.commit()
		con.close()
		list_layer = arcpy.mapping.ListLayers(mxd,view_name_in,df)
		for layer in list_layer:
			arcpy.mapping.RemoveLayer(df,layer)
		target_folder = 'Database Connections\spatial_view.sde'	
		arcpy.RefreshCatalog(target_folder)	
		arcpy.RefreshTOC()
		arcpy.RefreshActiveView()
	except:
		print 'could not delete view'

		
# remove distance/store profile and reset view
def resetview(view_name_in):
	try:
		view_space = view_name_in.find('svw')
		view_name = view_name_in[view_space:]
		con = dbconn()
		cur = con.cursor()
		sql_command = """EXEC [dbo].[gis_reset_view] '%s'""" % view_name
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'could not reset view'
		

# ********************************************************sync map to grid functions****************************************************
# reset selected field to 0
def syncmapupdate(view_name_in):
	try:
		view_space = view_name_in.find('svw')
		view_name = view_name_in[view_space:]
		con = dbconn()
		cur = con.cursor()
		sql_command = """EXEC [dbo].[gis_sync_map_update] '%s'""" % view_name
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'error'

	
# set selected = 1 for selected features in arcmap	
def syncmapset(view_name_in,geo_in):
	try:
		view_space = view_name_in.find('svw')
		view_name = view_name_in[view_space:]
		geo = str(geo_in)
		con = dbconn()
		cur = con.cursor()
		sql_command = """EXEC [dbo].[gis_sync_map_set] '%s','%s'""" % (view_name, geo)
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'error'
	
	
# # delete rows where selected = 0
def syncmapdelete(view_name_in):
	try:
		view_space = view_name_in.find('svw')
		view_name = view_name_in[view_space:]
		con = dbconn()
		cur = con.cursor()
		sql_command = """EXEC [dbo].[gis_sync_map_delete] '%s'""" % view_name
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'error'

		
# Loop through selected features and set "selected" field to 1 
def syncmaprun(view_name_in):
	try:
		# determine level of geography
		view_space = view_name_in.find('svw')
		view_name = view_name_in[view_space:]
		if view_name[0:4].upper() == 'SVWZ':
			featureclass = view_name_in
			rows = arcpy.SearchCursor(featureclass)
			row = rows.next()
			while row:
				zip = row.zip
				syncmapset(view_name_in,zip)
				row = rows.next()
		if view_name[0:4].upper() == 'SVWS':
			featureclass = view_name_in
			rows = arcpy.SearchCursor(featureclass)
			row = rows.next()
			while row:
				zip_split = row.zip_split
				syncmapset(view_name_in,zip_split)
				row = rows.next()
		if view_name[0:4].upper() == 'SVWR':
			featureclass = view_name_in
			rows = arcpy.SearchCursor(featureclass)
			row = rows.next()
			while row:
				CR_ID = row.CR_ID
				syncmapset(view_name_in,CR_ID)
				row = rows.next()
	except:
		print 'error'

		
# clear selected features and refresh map view		
def clearlayer(view_clear):
	try:
		arcpy.RefreshTOC()
		arcpy.RefreshActiveView()
		layers = arcpy.mapping.ListLayers(mxd,view_clear,df)
		for layer in layers:
			arcpy.SelectLayerByAttribute_management(layer,"CLEAR_SELECTION")		
	except:
		print 'error'

# **************************delete spatial view features using query**************************
def viewquery(view_name_in,sql_in):
	try:
		view_space = view_name_in.find('svw')
		table_name = 'tbl' + view_name[3:]
		con = dbconn()
		cur = con.cursor()
		sql_command = 'DELETE FROM ' + table_name + ' WHERE ' + sql_in
		arcpy.AddMessage(sql_command)
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'error'
		
		
		
		
		
		
# ***********************************************Profile Functions**********************************
# profile location unduplicated
def profileloc(loc_table_in,view_name_in,max_radius):
	try:
		view_space = view_name_in.find('svw')
		view_name = view_name_in[view_space:]
		table_name = 'tbl' + view_name[3:]
		con = dbconn()
		cur = con.cursor()
		rows = arcpy.SearchCursor(loc_table_in)
		row = rows.next()
		dupes = 'no'
		while row:
			store = row.store
			lat = row.latitude
			lon = row.longitude
			sql_command = """EXEC [dbo].[gis_SearchRadius_brian] '%s','%s','%s','%s','%s','%s'""" %(table_name, str(lat), str(lon), str(max_radius), str(store), dupes)
			cur.execute(sql_command)
			con.commit()
			row = rows.next()
		con.close()
		arcpy.AddMessage('Single Profile Complete')
	except:
		print 'profile failed'
		arcpy.AddMessage('Profile FAIL')

# profile locations with duplication		
def duplprofileloc(loc_table_in,view_name_in,max_radius):
	try:
		view_space = view_name_in.find('svw')
		view_name = view_name_in[view_space:]
		table_name = 'tbl' + view_name[3:]
		con = dbconn()
		cur = con.cursor()
		rows = arcpy.SearchCursor(loc_table_in)
		row = rows.next()
		dupes = 'no'
		while row:
			store = row.store
			lat = row.latitude
			lon = row.longitude
			sql_command = """EXEC [dbo].[gis_RadiusDupes_brian] '%s','%s','%s','%s','%s','%s'""" %(table_name, str(lat), str(lon), str(max_radius), str(store), dupes)
			cur.execute(sql_command)
			con.commit()
			row = rows.next()
		con.close()
		arcpy.AddMessage('Duplicated Profile Complete')
	except:
		print 'FAIL'
		arcpy.AddMessage('Duplicated Profile FAIL')
		
		
		
# *********************************************location functions****************************************************

# create new mdb
def newmdb(new_mdb_loc,new_mdb_name):
	try:
		arcpy.CreatePersonalGDB_management(new_mdb_loc,new_mdb_name)
		arcpy.AddMessage('Database Crested')
		space = new_mdb_loc + '/' + new_mdb_name
		return space;
	except:
		arcpy.AddMessage('fail')
		
# create location layer from geocoded table
def loctable(loc_in,space,loc_table,xy_event):
	try:
		arcpy.TableToTable_conversion(loc_in,space,loc_table)
		arcpy.MakeXYEventLayer_management(loc_in,"LONGITUDE","LATITUDE",xy_event,sr)
		arcpy.CopyFeatures_management(xy_event,loc_out)
		arcpy.Delete_management(xy_event)
		arcpy.Delete_management(loc_table)
		loc_layer = arcpy.mapping.Layer(loc_out)
		arcpy.mapping.AddLayer(df,loc_layer)
		arcpy.RefreshTOC()
		arcpy.RefreshActiveView()
	except:
		arcpy.AddMessage('error')
