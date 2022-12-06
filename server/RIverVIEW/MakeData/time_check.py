import time
import datetime

class time_chk:
    def __init__(self, s, DEBUG=1):
        self.__timeblock = s
        self.__entire_start=0
        self.__start = 0
        self.__end = 0
        self.__sec = 0
        self.__cnt = 0
        self.DEBUG = DEBUG
        self.__isnew = 0

    def start(self):
        if self.DEBUG == 0:
            return

        if self.__isnew == 0:
            self.__cnt = 0
            self.__isnew = 1
            self.__entire_start = time.time()
            self.__start = time.time()
            print('\n\n************************************************************')
            print((self.__timeblock).center(50))
            print()
        else:
            self.__isnew = 2
            self.__start = time.time()
        return self.__entire_start

    def end(self):
        if self.DEBUG == 0:
            return
        if self.__isnew == 1:
            self.__end = time.time()
            self.__sec = self.__end-self.__start
            print(self.__cnt,' 걸린시간 : ',end='')
            print(str(datetime.timedelta(seconds=self.__sec))[:10],end='\t\t')
            print('  시작부터 ', str(self.__end-self.__entire_start)[:5],'s')
        else:
            self.__end = time.time()
            self.__sec = self.__end-self.__start
            print(self.__cnt,' 걸린시간 : ',end='')
            print(str(datetime.timedelta(seconds=self.__sec))[:10],end='\t\t')
            print('  시작부터 ', str(self.__end-self.__entire_start)[:5],'s')
        self.__cnt += 1
        return self.__timeblock

    def eend(self, entirestart, timeblock):
        if self.DEBUG == 0:
            return
        self.__end = time.time()
        self.__sec = self.__end-entirestart
        print('************************************************************')
        print((timeblock+' 걸린시간 : '+str(datetime.timedelta(seconds=self.__sec))[:10]).ljust(40),end='')
        print(str(self.__sec)[:6],'s')
        print('\n\n')

    
    def cut(self, timeblock=''):
        print(timeblock.center(50))
        self.end()
        self.start()
        
