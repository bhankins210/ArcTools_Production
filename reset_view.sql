USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_spatialview_combined]    Script Date: 03/17/2016 13:19:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[gis_reset_view](@spatial_view nvarchar(50))
--example: EXEC [dbo].[gis_reset_view] 'svwz_r64614444'
AS

BEGIN

CREATE TABLE #temp_distance
(
	zip char(5),
	distance float
);



DECLARE @min_distance nvarchar(150)
DECLARE @delete_dupes nvarchar(100)
DECLARE @update_distance nvarchar(50)
DECLARE @length nvarchar(50)
DECLARE @substring_text nvarchar(50)
DECLARE @update_store nvarchar(50)
DECLARE @view_table nvarchar(50)


SET @length = len(@spatial_view) 
SET @substring_text = SUBSTRING(@spatial_view,4,cast(@length as int))
SET @view_table = 'tbl' + @substring_text
SET @min_distance = 'INSERT INTO #temp_distance (zip, distance) SELECT zip, MIN(distance) FROM ' + @view_table + ' GROUP BY zip' 
SET @delete_dupes = 'DELETE FROM ' + @view_table + ' WHERE (zip + distance) NOT IN (SELECT zip + distance FROM #temp_distance)' 
SET @update_distance = 'UPDATE ' + @view_table + ' SET distance = NULL'
SET @update_store = 'UPDATE ' + @view_table + ' SET store = NULL'

EXECUTE (@min_distance)
EXECUTE (@delete_dupes)
EXECUTE (@update_distance)
EXECUTE (@update_store)


END


