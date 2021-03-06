USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_SearchRadius_brian]    Script Date: 03/25/2016 14:14:33 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[gis_SearchRadius_brian](@tbl varchar(50), @lat float, @lon float, @maxr float, @st char(50), @dupes char(3)) AS

	set nocount on

	declare @sql char(1000)
	declare @a varchar(50), @o varchar(50)
	declare @src varchar(50)
    declare @where varchar(100)
    declare @from varchar(100)
	declare @londistance varchar(50)
	declare @latdistance varchar(50)

	set @latdistance = convert(varchar(50),69.047)
	set @londistance = convert(varchar(50),dbo.GetLongitudeDistance(@lat))
	

	-- Setup some shortcuts
	set @a = convert(varchar(50),@lat)
	set @o = convert(varchar(50),@lon)
	if substring(@tbl,1,4)='tblz'
     BEGIN
		set @src = ' [map_data].dbo.zip_polygon '
        set @where = ' where a.zip=b.zip '
     END
	if substring(@tbl,1,4)='tbls'
	BEGIN
		set @src = ' [map_data].dbo.tpz_polygon '
		set @where = ' where b.TPZ = a.zip_split '
	END
	if substring(@tbl,1,4)='tblr'
	BEGIN
		set @src = '[map_data].dbo.route_polygon'
		set @where = ' where b.CR_ID = a.CR_ID '
    END 

	-- Now create the update statement
	set @sql = 'update a
				set a.store=''' + rtrim(cast(@st as varchar(50))) + ''', a.distance=dbo.getdistance(' + @a + ',' + @o + ',b.latitude,b.longitude)
				from dbo.' + @tbl + ' a, ' + @src + ' b
				'+ @where +'
				and b.latitude < ('+@a+' + ((('+convert(varchar(50),@maxr)+'*2)/'+@latdistance+')*1)) and b.latitude > ('+@a+' - ((('+convert(varchar(50),@maxr)+'*2)/'+@latdistance+')*1)) and b.longitude < ('+@o+' + ((('+convert(varchar(50),@maxr)+'*2)/'+@londistance+')*1)) and b.longitude > ('+@o+' - ((('+convert(varchar(50),@maxr)+'*2)/'+@londistance+')*1)) and isnull(a.distance, 99999.0) > dbo.getdistance(' + @a + ',' + @o + ',b.latitude,b.longitude)
				and dbo.getdistance(' + @a + ',' + @o + ',b.latitude,b.longitude) <= ' + convert(varchar(50),@maxr)
--	print @sql
	exec (@sql)



