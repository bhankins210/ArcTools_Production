USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_Clean_View]    Script Date: 03/25/2016 14:13:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


-- EXEC sdeadmin.gis_Clean_View  'sdeadmin.tbls_R13414'

ALTER procedure [dbo].[gis_Clean_View] (@view as varchar (100))
AS
DECLARE @sql as varchar(1000)


--delete hybrid
SET @sql =	'delete ' + @view  + ' where market_code like ''%HYBD'''
EXEC(@sql)


--delete solo where there is shared
SET @sql =	'delete ' + @view  + ' where event_id = ''solo'' and zip in (select zip from ' + @view + ' where event_id <> ''solo'')'
EXEC(@sql)


--keep earliest and mailsouth over solo or complimentors
SET @sql =	'delete a from ' + @view  + ' a 
	inner join (select * from
	(select Zip, inhome_date, ranking, Rank() over (Partition BY Zip order by ranking, inhome_date desc)
	as rank from ' + @view  + ' where event_id <> ''solo'' )tmp
	where Rank =1) b on a.zip = b.zip and (a.inhome_date<>b.inhome_date or a.ranking<>b.ranking)'
EXEC(@sql)

