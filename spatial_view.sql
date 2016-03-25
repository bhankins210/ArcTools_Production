USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_spatialview_combined]    Script Date: 03/25/2016 14:14:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[gis_spatialview_combined](@view_datatable nvarchar(50),@start_date nvarchar(50),@end_date nvarchar(50),@view_spatialtable nvarchar(50),@states nvarchar(200))
--example: exec [dbo].[gis_spatialview_combined] 'tbls_r64691234','03/15/2016','07/01/2016','svws_r64691234','(''al'',''ms'',''ga'')'
AS

begin
declare @create_data_table char(300)
declare @add_fields char(300)
declare @add_PK char(300)
declare @update_selected char(300)
declare @create_spatialview char(300)
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
	--set @polygon_table = 'dbo.route_polygon'
	set @polygon_table = '[map_data].dbo.route_polygon_proj'
	set @where = 'b.CR_ID = a.CR_ID'
END 


if @states != '()'
BEGIN
	set @create_data_table = 
		'SELECT * INTO dbo.' + @view_datatable + 
		' FROM ' + @mapping_data_table + 
		' WHERE [state] IN ' + @states + 
		' AND(inhome_date >= ' + '''' + @start_date + '''' + 
		' AND inhome_date <= ' + '''' + @end_date + '''' + 
		' OR inhome_date IS NULL)'
END


if @states = '()'
BEGIN
	set @create_data_table = 
		'SELECT * INTO dbo.' + @view_datatable + 
		' FROM ' + @mapping_data_table + 
		' WHERE inhome_date >= ' + '''' + @start_date + '''' + 
		' AND inhome_date <= ' + '''' + @end_date + '''' + 
		' OR inhome_date IS NULL'
END	


set @add_fields = 
	'ALTER TABLE dbo.' + @view_datatable + ' ADD ID INT IDENTITY, selected bit,userSelect varchar(50),store varchar(50),distance float'

set @add_PK =
	 'ALTER TABLE dbo.' + @view_datatable + ' ADD CONSTRAINT ' + @constraint + ' PRIMARY KEY(ID,event_id)'
set @update_selected = 
	'UPDATE dbo.' + @view_datatable + ' SET selected = 0'
set @create_spatialview = 
	'CREATE VIEW ' + @view_spatialtable + '	AS SELECT a.*, b.OBJECTID, b.SHAPE FROM '+ @view_datatable + ' a JOIN ' + @polygon_table + ' b ON ' + @where

execute (@create_data_table)
execute (@add_fields)
execute (@add_PK)
execute (@update_selected)
execute (@create_spatialview)

--print (@create_data_table)
--print (@add_fields)
--print (@add_PK)
--print (@update_selected)
--print (@create_spatialview)

end
