USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_reset_view]    Script Date: 03/25/2016 14:13:55 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[gis_reset_view](@spatial_view nvarchar(50))
--example: EXEC [dbo].[gis_reset_view] 'svwz_r64614444'
AS


--CREATE TABLE #temp_distance
--(
--	zip char(5),
--	distance float
--)

BEGIN


--DECLARE @min_distance nvarchar(150)
DECLARE @delete_dupes nvarchar(200)
DECLARE @update_distance nvarchar(50)
DECLARE @length nvarchar(50)
DECLARE @substring_text nvarchar(50)
DECLARE @update_store nvarchar(50)
DECLARE @view_table nvarchar(50)
DECLARE @geo nvarchar(9)



SET @length = len(@spatial_view) 
SET @substring_text = SUBSTRING(@spatial_view,4,cast(@length as int))
SET @view_table = 'tbl' + @substring_text

if substring(@view_table,1,4)='tblz'
 BEGIN
	SET @geo = 'zip'
 END
if substring(@view_table,1,4)='tbls'
BEGIN
	SET @geo = 'zip_split'
END
if substring(@view_table,1,4)='tblr'
BEGIN
	SET @geo = 'CR_ID'
END 


--SET @min_distance = 'INSERT INTO #temp_distance (zip, distance) SELECT zip, MIN(distance) FROM ' + @view_table + ' GROUP BY zip' 
SET @delete_dupes = 'DELETE FROM ' + @view_table + ' WHERE ' + @geo + ' +  CAST(distance as nvarchar(20)) NOT IN (SELECT ' + @geo + ' + CAST(MIN(distance) as nvarchar(20)) FROM ' + @view_table + ' GROUP BY ' + @geo + ')' 
SET @update_distance = 'UPDATE ' + @view_table + ' SET distance = NULL'
SET @update_store = 'UPDATE ' + @view_table + ' SET store = NULL'

--EXECUTE (@min_distance)
EXECUTE (@delete_dupes)
EXECUTE (@update_distance)
EXECUTE (@update_store)

PRINT @delete_dupes

END
