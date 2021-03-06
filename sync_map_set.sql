USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_sync_map_set]    Script Date: 03/25/2016 14:15:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[gis_sync_map_set](@spatial_view nvarchar(50), @geo char(9))
--example: exec [dbo].[gis_sync_map_set] 'tblr_R44444444','35043R001'
AS

begin

declare @view_table nvarchar(50)
declare @length nvarchar(50)
declare @substring_text nvarchar(50)
declare @update_table nvarchar(125)
declare @where nvarchar(50)



set @length = len(@spatial_view) 
set @substring_text = SUBSTRING(@spatial_view,4,cast(@length as int))
set @view_table = 'tbl' + @substring_text

if substring(@view_table,1,4)='tblz'
 BEGIN
    set @where = 'rtrim(zip) = ' + '''' + rtrim(@geo) + ''''
 END
if substring(@view_table,1,4)='tbls'
BEGIN
	set @where = 'rtrim(zip_split) = ' + '''' + rtrim(@geo) + ''''
END
if substring(@view_table,1,4)='tblr'
BEGIN
	set @where = 'rtrim(CR_ID) = ' + '''' + rtrim(@geo) + ''''
END 

set @update_table = 'UPDATE ' + @view_table + ' SET selected = 1 WHERE ' + @where  


--print @update_table
execute (@update_table)


end