import pymssql

import os


class DataBase(object):

    def __init__(self, database):

        # 连接服务器地址
        server = "10.10.10.112"
        # 连接帐号
        user = "sa"
        # 连接密码
        password = "abc-123"
        # 数据库名称
        self.database_name1 = "WorkForce14Demo_peter"
        self.database_name2 = "Workflow86Demo"

        self.bak_path = 'C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\Backup\{0}.bak'.format(self.database_name1)

        if database == 1:
            # 获取连接
            self.conn = pymssql.connect(server, user, password, "master")
        elif database == 2:

            self.conn = pymssql.connect(server, user, password, self.database_name1)

        self.conn.autocommit(True)

        # 获取光标
        self.cursor = self.conn.cursor()

    def __del__(self):

        self.conn.autocommit(False)
        self.cursor.close()
        self.conn.close()

    def database_backup(self):
        try:
            self.cursor.execute("backup database WorkForce14Demo to disk='{0}'".format(self.bak_path))
            print('备份数据库成功')
        except Exception as e:
            print('备份数据库失败')
            raise e

    def database_restore(self):

        self.cursor.execute("select * From master.dbo.sysdatabases where name='{0}'".format(self.database_name1))
        stat = self.cursor.fetchone()
        if stat is None:
            print('该数据库不存在，即将进行新建还原操作')
            print('>>>>>')

            try:
                self.cursor.execute("""
               restore database {0} from DISK='C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\Backup\{1}' with replace,
               MOVE 'HRM86Demo' to 'C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\DATA\{0}.mdf',
               MOVE 'HRM86Demo_log' to  'C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\DATA\{0}.ldf'
                """.format(self.database_name1, 'WorkForce14Demo_peter.bak'))
                print('新建还原数据库成功')

            except Exception as e:
                print('新建还原数据库失败')
                raise e

        else:
            print('该数据库已存在，即将进行覆盖操作')
            print('数据库还原开始：')
            print('>>>>>')
            try:
                self.cursor.execute("""
                ALTER DATABASE {1} SET OFFLINE WITH ROLLBACK IMMEDIATE
                restore database {1} from DISK='C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\Backup\{1}.bak' with replace
                                               
                
                ALTER DATABASE {0} SET OFFLINE WITH ROLLBACK IMMEDIATE
                restore database {0} from DISK='C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER\MSSQL\Backup\{0}.bak' with replace
                
                """.format(self.database_name1, self.database_name2))
                print('数据库还原成功')

            except Exception as e:
                print('数据库还原失败')
                raise e

    def execute_sql(self, path=r"F:\wfm_flow\unit"):
        """执行指定目录下的.sql文件"""
        os.chdir(path)
        try:
            for each in os.listdir("."):
                count = 0   # 读取行数
                sql = ""    # 拼接的sql语句
                if "schedul.sql" in each:
                    with open(each, "r", encoding="utf-8") as f:
                        for each_line in f.readlines():
                            # 过滤数据
                            if not each_line or each_line == "\n":
                                continue
                            # 读取2000行数据，拼接成sql
                            elif count < 2000:
                                sql += each_line
                                count += 1
                            # 读取达到2000行数据，进行提交，同时，初始化sql，count值
                            else:
                                self.cursor.execute(sql)
                                sql = each_line
                                count = 1
                        # 当读取完毕文件，不到2000行时，也需对拼接的sql 执行、提交
                        if sql:
                            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        finally:
            print('sql文件执行完毕')
        return '排班sql执行了'


if __name__ == '__main__':
    DataBase(1).database_restore()
    # DataBase(2).execute_sql()
    # DataBase(1).database_backup()

