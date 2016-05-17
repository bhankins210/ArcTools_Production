import arcpy
import msparkdb

# input parameters	
index_string = arcpy.GetParameterAsText(0)
view_name_in = arcpy.GetParameterAsText(1)

# find table view name
view_space = view_name_in.find('svw')
view_name = view_name_in[view_space:]
table_name = 'tbl' + view_name[3:]

# # conver string of variables to tuple
# index_string = index_string.upper()
# index_tuple = tuple(index_string.split(','))

# connect to spatial_view DB
# con = msparkdb.dbconn()
# cur = con.cursor()

# def compositeindex(table_name, index_tuple):
	# try:
		# con = msparkdb.dbconn()
		# cur = con.cursor()
		# # add column to table for each variable
		# for index in index_tuple:
			# sql_command = 'ALTER TABLE ' + table_name + ' ADD ' + index + ' float'  
			# arcpy.AddMessage(sql_command)
			# cur.execute(sql_command)
			# sql_command4 = """EXEC [gis].[AddCompositeIndex]'%s','%s'""" %(table_name,index)
			# cur.execute(sql_command4)
			# con.commit()
		# # add composite_index to table
		# sql_command2 = 'ALTER TABLE ' + table_name + ' ADD composite_index float'  
		# cur.execute(sql_command2)
		# con.commit()

		# index_string_repl = index_string.replace(',','+')
		# tup_len = len(index_tuple)
		# sql_command5 = 'UPDATE ' + table_name + ' SET composite_index = (' + index_string_repl + ')/' + str(tup_len)
		# cur.execute(sql_command5)
		# con.commit()
		# arcpy.AddMessage(sql_command5)

		 

		# # refresh view on sql db and close connection
		# sql_command3 = "EXECUTE sp_refreshview N'sde." + view_name + "'"
		# arcpy.AddMessage(sql_command3)
		# cur.execute(sql_command3)
		# con.commit()
		# con.close()
	# except:
		# arcpy.AddMessage('Failed to add Composite Index')

msparkdb.compositeindex(table_name,index_string)

	

