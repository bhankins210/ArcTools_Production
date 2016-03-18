"""
Spatial View Function Module

"""

import arcpy
import pypyodbc


# define working mxd file, data frame, and sde connection
mxd = arcpy.mapping.MapDocument(r"CURRENT")
df = arcpy.mapping.ListDataFrames(mxd,'*')[0]	
db_connection = 'Database Connections\spatial_view.sde'


# Creates databse connection via pypyodbc
def dbconn():
	try:
		connection = pypyodbc.connect('DRIVER={SQL Server};SERVER=mapping-sqldev\esri;DATABASE=spatial_view;UID=id;PWD=pass;Trusted_Connection=Yes')
		return connection
	except:
		print 'Cannot connect to database'
		
		
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
		
		
