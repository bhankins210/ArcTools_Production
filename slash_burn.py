import arcpy 
from arcpy import env 
import os 
import msparkdb

# Establish connection for workspace 

delete_all = arcpy.GetParameterAsText(0)

env.workspace = 'Database Connections\\spatial_view.sde\\'	

#call ListFeatureClass function
if delete_all == 'true':
	fcList = arcpy.ListFeatureClasses()

# Print the name of the current fc:
	for fc in fcList:
		arcpy.AddMessage(fc)
		msparkdb.deleteview(fc)
		
arcpy.RefreshTOC()
arcpy.RefreshActiveView()
	