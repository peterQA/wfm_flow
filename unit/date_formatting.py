import datetime


class FormatTime(object):

    def time_of_day(self, _time=''):
        # 当日时间 格式：2019-08-30 11:00:00
        # time_of_day = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_day = datetime.datetime.now().strftime('%Y-%m-%d {0}'.format(_time))
        print('当日时间', time_day)
        return time_day

    def next_of_day(self, _time=""):
        # 次日时间 格式：2019-08-31 11:00:00
        next_day = (datetime.datetime.now() + datetime.timedelta(hours=24, minutes=00, seconds=00))\
            .strftime('%Y-%m-%d {0}'.format(_time))
        print('次日时间', next_day)
        return next_day


if __name__ == '__main__':
    ft = FormatTime()
    ft.next_of_day("18:00:00")
    ft.next_of_day()



