USE [spatial_view]
GO
/****** Object:  StoredProcedure [dbo].[gis_RadiusDupes_brian]    Script Date: 03/25/2016 14:13:33 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER proc [dbo].[gis_RadiusDupes_brian] (@tbl varchar(50), @lat float, @lon float, @maxr float, @st varchar(50), @dupes char(3)) AS
--exec [dbo].[gis_RadiusDupes] 'tblz_r13584','32.297781','-90.229982','10','Gateway Tire & Service Ctr. #64','no'

declare @columnlist as varchar(3000)
declare @currentcolumn as varchar(100)
declare @length as int 
declare @sql char(3000)
declare @a varchar(50), @o varchar(50)
declare @src varchar(50)
declare @where varchar(100)
declare @from varchar(100)
declare @londistance varchar(50)
declare @latdistance varchar(50)

set @currentcolumn = ''
set @columnlist = ''
set @length = 0

set @latdistance = convert(varchar(50),69.047)
set @londistance = convert(varchar(50),dbo.GetLongitudeDistance(@lat))

--Step 1. Set Up Shortcuts

	set @a = convert(varchar(50),@lat)
	set @o = convert(varchar(50),@lon)
	if substring(@tbl,1,4)='tblz'
     BEGIN
		set @src = ' [map_data].dbo.zip_polygon '
        set @where = ' a.zip = b.zip '
     END
	if substring(@tbl,1,4)='tbls'
	BEGIN
		set @src = ' [map_data].dbo.tpz_polygon '
		set @where = ' b.TPZ = a.zip_split '
	END
	if substring(@tbl,1,4)='tblr'
	BEGIN
		set @src = '[map_data].dbo.route_polygon'
		set @where = ' b.CR_ID = a.CR_ID '
    END 


--Step 2. Select column to be used in insert statement

SELECT o.name AS tableName, c.name AS columnName, c.colorder as colorder INTO #Columns
FROM dbo.syscolumns c
INNER JOIN dbo.sysobjects o
ON c.id = o.id
WHERE o.name = @tbl and c.name <> 'id'
ORDER BY c.colorder

--Step 3. Create list of columns in a string

while exists(select * from #columns)
	   BEGIN
			select top 1 @currentcolumn = columnName from #columns order by colorder
			if @currentcolumn = 'distance'
				BEGIN
					set @columnlist = @columnlist + ' dbo.getdistance('''+@a+''','''+@o+''',b.latitude,b.longitude),'
				END
			else if @currentcolumn = 'store'
				BEGIN
					set @columnlist = @columnlist + ' ''' + @st + ''','
				END
			else 
				BEGIN
					set @columnlist = @columnlist + ' a.' +@currentcolumn + ','
				END
			delete from #columns where columnName = @currentcolumn
	   END
--print @columnlist
--Step 4. Clean up @columnlist

set @length = len(@columnlist)-1
set @columnlist = left(@columnlist,@length)


--Step 5. Write Insert Statment

set @sql = 'insert into dbo.' + @tbl +
		   ' select distinct' + @columnlist +
		   ' from dbo.' + @tbl + ' a,' + @src + ' b ' +
		   ' where b.latitude < ('+@a+' + ((('+convert(varchar(50),@maxr)+'*2)/'+@latdistance+')*1)) and b.latitude > ('+@a+' - ((('+convert(varchar(50),@maxr)+'*2)/'+@latdistance+')*1)) and b.longitude < ('+@o+' + ((('+convert(varchar(50),@maxr)+'*2)/'+@londistance+')*1)) and b.longitude > ('+@o+' - ((('+convert(varchar(50),@maxr)+'*2)/'+@londistance+')*1)) and dbo.getdistance(''' + @a + ''',''' + @o + ''',b.latitude,b.longitude) < ' + convert(varchar(50),@maxr) + ' and' + @where + 
		   ' and a.store <> ''' + @st + ''' and dbo.getdistance(''' + @a + ''',''' + @o + ''',b.latitude,b.longitude) >= a.distance'

--Step 6. Execute Insert Statement
--
	--print @sql
	exec (@sql)




	

