USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_sync_map_delete]    Script Date: 03/25/2016 14:15:07 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[gis_sync_map_delete](@spatial_view nvarchar(50))
--example: exec [dbo].[gis_sync_map_delete] 'svwr_R44444444'
AS

begin

declare @view_table nvarchar(50)
declare @length nvarchar(50)
declare @substring_text nvarchar(50)
declare @update_table nvarchar(50)

set @length = len(@spatial_view) 
set @substring_text = SUBSTRING(@spatial_view,4,cast(@length as int))
set @view_table = 'tbl' + @substring_text
set @update_table = 'DELETE FROM ' + @view_table + ' WHERE selected = 0'

--print (@update_table)
execute (@update_table)


end



