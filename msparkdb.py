"""
Spatial View Function Module

"""

import pypyodbc
import arcpy

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
		arcpy.MakeQueryLayer_management(db_connection,view_name,select_query,"ID","POLYGON")
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

# runs spatial view stored procedure - all states		
def allstateview(*in_var):
	try:
		sql_param_tup = in_var
		con = dbconn()
		cur = con.cursor()
		sql_command = """EXEC [dbo].[gis_spatialview_all_states] '%s','%s','%s','%s'""" % (sql_param_tup)
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'could not create view'

def selectstateview(*in_var):
	try:
		sql_param_tup = in_var
		con = dbconn()
		cur = con.cursor()
		sql_command = """EXEC [dbo].[gis_spatialview_state_list] '%s','%s','%s','%s','%s'""" % (sql_param_tup)
		cur.execute(sql_command)
		con.commit()
		con.close()
	except:
		print 'could not create view'

		