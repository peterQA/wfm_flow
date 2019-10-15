	declare @yearFirstDay datetime  --年度第一天
	declare @yearLastDay datetime   --年度最后一天
	declare @monthFirstday datetime --当前月第一天
	declare @monthLastday datetime  --当前月最后一天
	declare @userid nvarchar(38) --创建用户
	declare @workhourid int=2     --工时id
	set @yearFirstDay = dateadd(year, datediff(year, 0, getdate()), 0)
	set @yearLastDay = dateadd(year, datediff(year, 0, dateadd(year, 1, getdate())), -1)
	set @monthFirstday = DATEADD(DAY,0,DATEADD(MM,DATEDIFF(MM,0,GETDATE())+0,0))
	set @monthLastday = DATEADD(DAY,-1,DATEADD(MM,DATEDIFF(MM,0,GETDATE())+1,0))
	set @userid = '0000010012'


	---排班 默认排系统时间当月的班次 默认排早班 时间为06:00-15:00
	declare @date datetime
	set @date = @monthFirstday
	while @date<@monthLastday
	begin
		---排班
		delete from empshift where userid=@userid and att_date = @date
		INSERT empshift(userid,att_date,workhourid1,typeid)
		SELECT @userid,@date,@workhourid,1
		set @date = DATEADD(DAY,1,@date)
	end
--录入员工系统当天打卡数据 迟到1小时
	if not exists(select 1 from atsoriginaldata where userid=@userid and cardtime = (select CONVERT(datetime,CONVERT(varchar(100), GETDATE(), 23)+ ' 07:00')))
	begin
		insert into atsoriginaldata(userid,cardtime,inorout,storecode,signtype,changedstatus) values (@userid,CONVERT(datetime,CONVERT(varchar(100), GETDATE(), 23) + ' 07:00'),1,'SHNo1',1,1)
	end

	--录入员工系统昨天打卡数据 加班2小时
	if not exists(select 1 from atsoriginaldata where userid=@userid and cardtime = (select CONVERT(datetime,CONVERT(varchar(100), dateadd(dd,-1,getdate()) , 23)+ ' 06:00')))
	begin
		insert into atsoriginaldata(userid,cardtime,inorout,storecode,signtype,changedstatus) values (@userid,CONVERT(datetime,CONVERT(varchar(100), dateadd(dd,-1,getdate()) , 23) + ' 06:00'),1,'SHNo1',1,1)
	end
	if not exists(select 1 from atsoriginaldata where userid=@userid and cardtime = (select CONVERT(datetime,CONVERT(varchar(100), dateadd(dd,-1,getdate()) , 23)+ ' 18:00')))
	begin
		insert into atsoriginaldata(userid,cardtime,inorout,storecode,signtype,changedstatus) values (@userid,CONVERT(datetime,CONVERT(varchar(100), dateadd(dd,-1,getdate()) , 23) + ' 18:00'),2,'SHNo1',1,1)
	end
