IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[usp_iris_prepare_data]'))
DROP PROCEDURE [dbo].[usp_iris_prepare_data]
GO
create PROCEDURE usp_iris_prepare_data
	@userid nvarchar(38), --创建用户
	@workhourid int=2     --工时id
	
	WITH ENCRYPTION
as 
BEGIN
	
	--基本设置 
	--年假 享有10天
	--休假政策： 管理人员  年假-匹配考勤
	--加班政策：管理人员  平日加班-匹配考勤    
	--                    周末加班-匹配日历 日期类型-休息
	--排班  当月份全排早班  时间为06:00-15:00

	--select * from employee1 where empcode='wfm001'
	--select * from employeewf where serialnumber='0000000021'
	--select * from empannualinfo where userid='0000010012'

	declare @yearFirstDay datetime  --年度第一天
	declare @yearLastDay datetime   --年度最后一天
	declare @monthFirstday datetime --当前月第一天
	declare @monthLastday datetime  --当前月最后一天
	set @yearFirstDay = dateadd(year, datediff(year, 0, getdate()), 0)
	set @yearLastDay = dateadd(year, datediff(year, 0, dateadd(year, 1, getdate())), -1)
	set @monthFirstday = DATEADD(DAY,0,DATEADD(MM,DATEDIFF(MM,0,GETDATE())+0,0))
	set @monthLastday = DATEADD(DAY,-1,DATEADD(MM,DATEDIFF(MM,0,GETDATE())+1,0))
	

	--加班政策 平日加班 匹配考勤
	update otclass_apply set matchtype=1 ,allowafterapply = 1,maxdelayapplydays =3 where otclasscode='Manager' and ottype='OT01'
	--加班政策  周末加班 匹配日历  日期类型-休息
	update otclass_apply set matchtype=0 ,date_type=1,allowafterapply = 1,maxdelayapplydays =3 where otclasscode='Manager' and ottype='OT02'
	
	--休假政策 年假  匹配考勤 
	update leaveclass_apply  set matchtype=1 where leaveclasscode='Manager' and leavetype='lv01'
	--设置wfm001的法定年假享有为10天
	if not exists (select 1 from empannualinfo where userid=@userid and year_begin_date=@yearFirstDay)
	begin
		insert into empannualinfo (userid,year_begin_date,year_end_date,calc_anlv_type,datasource,occurtotal,expire_date)
		values (@userid,@yearFirstDay,@yearLastDay,	0	,0	,10,@yearLastDay)
	end
	else
	begin
		delete from empannualinfo where userid=@userid and year_begin_date=@yearFirstDay 
		insert into empannualinfo (userid,year_begin_date,year_end_date,calc_anlv_type,datasource,occurtotal,expire_date)
		values (@userid,@yearFirstDay,@yearLastDay,	0	,0	,10,@yearLastDay)
	end

	--select * from workhourcls where atscode='ATSWFM_ML'
	
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
	
	--select   dateadd(dd,-1,getdate()) 
	--select DATEADD(DAY,0,DATEADD(MM,DATEDIFF(MM,0,GETDATE())+0,0))
	--Select CONVERT(varchar(30),getdate(),120) 
	--Select CONVERT(datetime,CONVERT(varchar(100), GETDATE(), 23) + ' 07:00') 

	-----给wfm001排班 默认排系统时间当月的班次 默认排早班 时间为06:00-15:00
	--set @date = @firstday
	--while @date<@lastday
	--begin
	--	---排班
	--	delete from empshift where userid='0000010012' and att_date = @date
	--	INSERT empshift(userid,att_date,workhourid1,typeid)
	--	SELECT '0000010012',@date,2,1
	--	set @date = DATEADD(DAY,1,@date)
	--end

	--select * from empshift where userid='0000010012'
	--delete from empshift where autoid=12787
	--delete from empshift where autoid=12788

	--select * from atsoriginaldata where userid='0000010012' order by cardtime
	--delete from atsoriginaldata where autoid=252000

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
	--if not exists (select 1 from atsoriginaldata where userid=@userid and cardtime = (select CONVERT(datetime,CONVERT(varchar(100), GETDATE(), 23)+ ' 15:00')))
	--begin
	--	insert into atsoriginaldata(userid,cardtime,inorout,storecode,signtype,changedstatus) values (@userid,CONVERT(datetime,CONVERT(varchar(100), GETDATE(), 23) + ' 15:00'),2,'SHNo1',1,1)
	--end
	
	--用户流程权限赋值
	declare @groupcode nvarchar(20)
	select @groupcode=groupcode from users where userid=@userid
	print @groupcode
	if not exists (select 1 from permissiongroup_objectrange where groupcode=@groupcode and objecttype='processcode' and objectid='onboard')
	begin
		insert into permissiongroup_objectrange(groupcode,objecttype,objectid,object_security) values (@groupcode,'processcode','onboard','11111111111111111111')
	end
	if not exists (select 1 from permissiongroup_objectrange where groupcode=@groupcode and objecttype='processcode' and objectid='overtime')
	begin
		print(1)
		insert into permissiongroup_objectrange(groupcode,objecttype,objectid,object_security) values (@groupcode,'processcode','overtime','11111111111111111111')
	end
	if not exists (select 1 from permissiongroup_objectrange where groupcode=@groupcode and objecttype='processcode' and objectid='Termination')
	begin
		insert into permissiongroup_objectrange(groupcode,objecttype,objectid,object_security) values (@groupcode,'processcode','Termination','11111111111111111111')
	end
	if not exists (select 1 from permissiongroup_objectrange where groupcode=@groupcode and objecttype='processcode' and objectid='wfmcancellate')
	begin
		insert into permissiongroup_objectrange(groupcode,objecttype,objectid,object_security) values (@groupcode,'processcode','wfmcancellate','11111111111111111111')
	end
	if not exists (select 1 from permissiongroup_objectrange where groupcode=@groupcode and objecttype='processcode' and objectid='wfmleave')
	begin
		insert into permissiongroup_objectrange(groupcode,objecttype,objectid,object_security) values (@groupcode,'processcode','wfmleave','11111111111111111111')
	end
	if not exists (select 1 from permissiongroup_objectrange where groupcode=@groupcode and objecttype='processcode' and objectid='wfmtimingcard')
	begin
		insert into permissiongroup_objectrange(groupcode,objecttype,objectid,object_security) values (@groupcode,'processcode','wfmtimingcard','11111111111111111111')
	end
	if not exists (select 1 from permissiongroup_objectrange where groupcode=@groupcode and objecttype='processcode' and objectid='wfmtransferstore')
	begin
		insert into permissiongroup_objectrange(groupcode,objecttype,objectid,object_security) values (@groupcode,'processcode','wfmtransferstore','11111111111111111111')
	end

	
	--修改繁体描述
	update parameters set t_name='離職' where paracode='QUITREASON' and itemcode='0001'
	update parameters set t_name='合同到期' where paracode='QUITREASON' and itemcode='0002'
	update parameters set t_name='test' where paracode='QUITREASON' and itemcode='0003'
	update parameters set t_name='解僱' where paracode='RS' and itemcode='01'
	update parameters set t_name='辭職' where paracode='RS' and itemcode='02'
	update parameters set t_name='退職' where paracode='RS' and itemcode='03'
	update parameters set t_name='病退' where paracode='RS' and itemcode='04'
	update parameters set t_name='內退' where paracode='RS' and itemcode='05'
	update ottype set t_name='平日加班' where code='OT01'
	update store set t_name='港匯廣場店' where code='SHNo1'

END
GO