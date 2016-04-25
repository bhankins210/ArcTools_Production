import arcpy
import msparkdb

# location table - after geocoding
loc_table_in = arcpy.GetParameterAsText(0)

# spatial view to profile
view_name_in = arcpy.GetParameterAsText(1)

# Maximum Distance
max_radius = arcpy.GetParameterAsText(2)

# Handle duplication
dupl = arcpy.GetParameterAsText(3)




# def duplprofileloc(loc_table_in,view_name_in,max_radius):
	# try:
		# view_space = view_name_in.find('svw')
		# arcpy.AddMessage('1')
		# view_name = view_name_in[view_space:]
		# arcpy.AddMessage('2')
		# table_name = 'tbl' + view_name[3:]
		# arcpy.AddMessage('3')
		# con = msparkdb.dbconn2()
		# arcpy.AddMessage('4')
		# cur = con.cursor()
		# arcpy.AddMessage('5')
		# rows = arcpy.SearchCursor(loc_table_in)
		# arcpy.AddMessage('6')
		# row = rows.next()
		# arcpy.AddMessage('7')
		# dupes = 'no'
		# arcpy.AddMessage('8')
		# while row:
			# store = row.store
			# arcpy.AddMessage(store)
			# lat = row.latitude
			# arcpy.AddMessage('10')
			# lon = row.longitude
			# arcpy.AddMessage('11')
			# sql_command = """EXEC [dbo].[gis_RadiusDupes_brian] '%s','%s','%s','%s','%s','%s'""" %(table_name, str(lat), str(lon), str(max_radius), str(store), dupes)
			# arcpy.AddMessage(sql_command)
			# cur.execute(sql_command)
			# arcpy.AddMessage('13')
			# con.commit()
			# arcpy.AddMessage('14')
			# row = rows.next()
			# arcpy.AddMessage('15')
		# con.close()
		# arcpy.AddMessage('16')
		# arcpy.AddMessage('Duplicated Profile Complete')
	# except:
		# print 'FAIL'
		# arcpy.AddMessage('Duplicated Profile FAIL')
		
		
		
		
# execute profile stored procedures
msparkdb.profileloc(loc_table_in,view_name_in,max_radius)
if str(dupl) == 'true':
	msparkdb.duplprofileloc(loc_table_in,view_name_in,max_radius)
	# duplprofileloc(loc_table_in,view_name_in,max_radius)


