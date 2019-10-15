IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[usp_iris_prepare_data]'))
DROP PROCEDURE [dbo].[usp_iris_prepare_data]
GO
create PROCEDURE usp_iris_prepare_data
	@userid nvarchar(38), --�����û�
	@workhourid int=2     --��ʱid
	
	WITH ENCRYPTION
as 
BEGIN
	
	--�������� 
	--��� ����10��
	--�ݼ����ߣ� ������Ա  ���-ƥ�俼��
	--�Ӱ����ߣ�������Ա  ƽ�ռӰ�-ƥ�俼��    
	--                    ��ĩ�Ӱ�-ƥ������ ��������-��Ϣ
	--�Ű�  ���·�ȫ�����  ʱ��Ϊ06:00-15:00

	--select * from employee1 where empcode='wfm001'
	--select * from employeewf where serialnumber='0000000021'
	--select * from empannualinfo where userid='0000010012'

	declare @yearFirstDay datetime  --��ȵ�һ��
	declare @yearLastDay datetime   --������һ��
	declare @monthFirstday datetime --��ǰ�µ�һ��
	declare @monthLastday datetime  --��ǰ�����һ��
	set @yearFirstDay = dateadd(year, datediff(year, 0, getdate()), 0)
	set @yearLastDay = dateadd(year, datediff(year, 0, dateadd(year, 1, getdate())), -1)
	set @monthFirstday = DATEADD(DAY,0,DATEADD(MM,DATEDIFF(MM,0,GETDATE())+0,0))
	set @monthLastday = DATEADD(DAY,-1,DATEADD(MM,DATEDIFF(MM,0,GETDATE())+1,0))
	

	--�Ӱ����� ƽ�ռӰ� ƥ�俼��
	update otclass_apply set matchtype=1 ,allowafterapply = 1,maxdelayapplydays =3 where otclasscode='Manager' and ottype='OT01'
	--�Ӱ�����  ��ĩ�Ӱ� ƥ������  ��������-��Ϣ
	update otclass_apply set matchtype=0 ,date_type=1,allowafterapply = 1,maxdelayapplydays =3 where otclasscode='Manager' and ottype='OT02'
	
	--�ݼ����� ���  ƥ�俼�� 
	update leaveclass_apply  set matchtype=1 where leaveclasscode='Manager' and leavetype='lv01'
	--����wfm001�ķ����������Ϊ10��
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
	
	---�Ű� Ĭ����ϵͳʱ�䵱�µİ�� Ĭ������� ʱ��Ϊ06:00-15:00
	declare @date datetime
	set @date = @monthFirstday
	while @date<@monthLastday
	begin
		---�Ű�
		delete from empshift where userid=@userid and att_date = @date
		INSERT empshift(userid,att_date,workhourid1,typeid)
		SELECT @userid,@date,@workhourid,1
		set @date = DATEADD(DAY,1,@date)
	end
	
	--select   dateadd(dd,-1,getdate()) 
	--select DATEADD(DAY,0,DATEADD(MM,DATEDIFF(MM,0,GETDATE())+0,0))
	--Select CONVERT(varchar(30),getdate(),120) 
	--Select CONVERT(datetime,CONVERT(varchar(100), GETDATE(), 23) + ' 07:00') 

	-----��wfm001�Ű� Ĭ����ϵͳʱ�䵱�µİ�� Ĭ������� ʱ��Ϊ06:00-15:00
	--set @date = @firstday
	--while @date<@lastday
	--begin
	--	---�Ű�
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

	--¼��Ա��ϵͳ��������� �ٵ�1Сʱ
	if not exists(select 1 from atsoriginaldata where userid=@userid and cardtime = (select CONVERT(datetime,CONVERT(varchar(100), GETDATE(), 23)+ ' 07:00')))
	begin
		insert into atsoriginaldata(userid,cardtime,inorout,storecode,signtype,changedstatus) values (@userid,CONVERT(datetime,CONVERT(varchar(100), GETDATE(), 23) + ' 07:00'),1,'SHNo1',1,1)
	end

	--¼��Ա��ϵͳ��������� �Ӱ�2Сʱ
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
	
	--�û�����Ȩ�޸�ֵ
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

	
	--�޸ķ�������
	update parameters set t_name='�x' where paracode='QUITREASON' and itemcode='0001'
	update parameters set t_name='��ͬ����' where paracode='QUITREASON' and itemcode='0002'
	update parameters set t_name='test' where paracode='QUITREASON' and itemcode='0003'
	update parameters set t_name='��l' where paracode='RS' and itemcode='01'
	update parameters set t_name='�o' where paracode='RS' and itemcode='02'
	update parameters set t_name='��' where paracode='RS' and itemcode='03'
	update parameters set t_name='����' where paracode='RS' and itemcode='04'
	update parameters set t_name='����' where paracode='RS' and itemcode='05'
	update ottype set t_name='ƽ�ռӰ�' where code='OT01'
	update store set t_name='�ۅR�V����' where code='SHNo1'

END
GO