USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_spatialview_combined]    Script Date: 03/29/2016 12:39:16 ******/
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
declare @geo nvarchar(9)
declare @add_index char(300)
declare @view_constraint nvarchar(50)

set @constraint = 'PK_' + @view_datatable
set @view_constraint = 'PK_' + @view_spatialtable


if substring(@view_datatable,1,4)='tblz'
 BEGIN
	set @mapping_data_table = '[map_data].dbo.tblmappingzipdata_cp'
	set @polygon_table = '[map_data].dbo.zip_polygon_prj'
    set @where = 'a.zip = b.zip'
    set @geo = 'zip'
 END
if substring(@view_datatable,1,4)='tbls'
BEGIN
	set @mapping_data_table = '[map_data].dbo.tblmappingsplitzipdata_cp'
	set @polygon_table = '[map_data].dbo.tpz_polygon_prj'
	set @where = 'b.TPZ = a.zip_split'
	set @geo = 'zip_split'
END
if substring(@view_datatable,1,4)='tblr'
BEGIN
	set @mapping_data_table = '[map_data].dbo.tblmappingroutedata_cp'
	--set @polygon_table = 'dbo.route_polygon'
	set @polygon_table = '[map_data].dbo.route_polygon_prj'
	set @where = 'b.CR_ID = a.CR_ID'
	set @geo = 'CR_ID'
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


--set @add_fields = 
--	'ALTER TABLE dbo.' + @view_datatable + ' ADD ID INT IDENTITY, selected bit,userSelect varchar(50),store varchar(50),distance float'

--set @add_PK =
--	 'ALTER TABLE dbo.' + @view_datatable + ' ADD CONSTRAINT ' + @constraint + ' PRIMARY KEY CLUSTERED(' + @geo + ',event_id)'
--set @update_selected = 
--	'UPDATE dbo.' + @view_datatable + ' SET selected = 0'
--set @create_spatialview = 
--	'CREATE VIEW ' + @view_spatialtable + '	AS SELECT a.' + @geo + ', a.event_id, a.hh_count, b.OBJECTID, b.SHAPE FROM '+ @view_datatable + ' a JOIN ' + @polygon_table + ' b ON ' + @where
----set @add_index = 
----	'CREATE UNIQUE CLUSTERED INDEX ' + @view_constraint + ' ON ' + @view_spatialtable + ' (' + @geo + ', event_id)'
------	'ALTER VIEW ' + @view_spatialtable + ' ADD CONSTRAINT ' + @view_constraint + ' PRIMARY KEY CLUSTERED(' + @geo + ', event_id)'

set @add_fields = 
	'ALTER TABLE dbo.' + @view_datatable + ' ADD VIEW_OID INT IDENTITY, selected bit,userSelect varchar(50),store varchar(50),distance float'

set @add_PK =
	 'ALTER TABLE dbo.' + @view_datatable + ' ADD CONSTRAINT ' + @constraint + ' PRIMARY KEY CLUSTERED(' + @geo + ',VIEW_OID)'
set @update_selected = 
	'UPDATE dbo.' + @view_datatable + ' SET selected = 0'
set @create_spatialview = 
	'CREATE VIEW ' + @view_spatialtable + ' AS SELECT a.VIEW_OID, a.' + @geo + ', a.event_id, a.hh_count,a.selected, a.store, a.distance, b.SHAPE FROM '+ @view_datatable + ' a JOIN ' + @polygon_table + ' b ON ' + @where

	 
execute (@create_data_table)
execute (@add_fields)
execute (@add_PK)
execute (@update_selected)
execute (@create_spatialview)
--execute (@add_index)

--print (@create_data_table)
--print (@add_fields)
--print (@add_PK)
--print (@update_selected)
--print (@create_spatialview)
----print (@add_index)

end


exec [dbo].[gis_spatialview_combined] 'tblr_r64691234z','03/15/2016','07/01/2016','svwr_r64691234z','(''al'',''ms'',''ga'')'
