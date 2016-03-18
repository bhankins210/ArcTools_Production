USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_spatialview_combined]    Script Date: 03/17/2016 13:19:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[gis_delete_spatialview](@spatial_view nvarchar(50))
--example: exec [dbo].[gis_delete_spatialview] 'svwr_R44444444'
AS

begin

declare @view_table nvarchar(50)
declare @drop_view nvarchar(50)
declare @drop_table nvarchar(50)
declare @length nvarchar(50)
declare @substring_text nvarchar(50)

set @length = len(@spatial_view) 
set @substring_text = SUBSTRING(@spatial_view,4,cast(@length as int))
set @view_table = 'tbl' + @substring_text
set @drop_view = 'DROP VIEW ' + @spatial_view
set @drop_table = 'DROP TABLE ' + @view_table

execute (@drop_view)
execute (@drop_table)

end



