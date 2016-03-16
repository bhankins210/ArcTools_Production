USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_spatialview_all_states]    Script Date: 03/14/2016 10:34:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[gis_spatialview_state_list](@view_datatable nvarchar(50),@states nvarchar(200),@start_date char(10),@end_date char(10),@view_spatialtable nvarchar(50))
--example: exec [dbo].[gis_spatialview_state_list] 'tbls_r64691234','(''al'',''ms'',''ga'')','03/15/2016','07/01/2016','svws_r64691234'
AS

begin
declare @sql_1 char(3000)
declare @sql_2 char(3000)
declare @sql_3 char(3000)
declare @sql_4 char(3000)
declare @sql_5 char(3000)
declare @constraint nvarchar(50)
declare @where nvarchar(100)
declare @polygon_table nvarchar(50)
declare @mapping_data_table nvarchar(50)

set @constraint = 'PK_' + @view_datatable



if substring(@view_datatable,1,4)='tblz'
 BEGIN
	set @mapping_data_table = '[map_data].dbo.tblmappingzipdata_cp'
	set @polygon_table = '[map_data].dbo.zip_polygon'
    set @where = 'a.zip = b.zip'
 END
if substring(@view_datatable,1,4)='tbls'
BEGIN
	set @mapping_data_table = '[map_data].dbo.tblmappingsplitzipdata_cp'
	set @polygon_table = '[map_data].dbo.tpz_polygon'
	set @where = 'b.TPZ = a.zip_split'
END
if substring(@view_datatable,1,4)='tblr'
BEGIN
	set @mapping_data_table = '[map_data].dbo.tblmappingroutedata_cp'
	set @polygon_table = '[map_data].dbo.route_polygon'
	set @where = 'b.CR_ID = a.CR_ID'
END 



set @sql_1 = 
	'SELECT * INTO dbo.' + @view_datatable + 
	' FROM ' + @mapping_data_table + 
	' WHERE [state] IN ' + @states + 
	' AND(inhome_date >= ' + '''' + @start_date + '''' + 
	' AND inhome_date <= ' + '''' + @end_date + '''' + 
	' OR inhome_date IS NULL)'
		
	

set @sql_2 = 
	'ALTER TABLE dbo.' + @view_datatable + ' ADD ID INT IDENTITY, selected bit,userSelect varchar(50),store varchar(50),distance float'

set @sql_3 =
	 'ALTER TABLE dbo.' + @view_datatable + ' ADD CONSTRAINT ' + @constraint + ' PRIMARY KEY(ID)'
set @sql_4 = 
	'UPDATE dbo.' + @view_datatable + ' SET selected = 0'
set @sql_5 = 
	'CREATE VIEW ' + @view_spatialtable + '	AS SELECT a.*, b.OBJECTID, b.SHAPE FROM '+ @view_datatable + ' a JOIN ' + @polygon_table + ' b ON ' + @where


--print @sql_1
--print @sql_2
--print @sql_3
--print @sql_4
--print @sql_5

execute (@sql_1)
execute (@sql_2)
execute (@sql_3)
execute (@sql_4)
execute (@sql_5)

end


