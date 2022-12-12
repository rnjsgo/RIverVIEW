import time
import os
import datetime

class p:
    class COLOR:
        BRIGHT_BLACK = '\033[90m'
        BRIGHT_RED = '\033[91m'
        BRIGHT_GREEN = '\033[92m'
        BRIGHT_YELLOW = '\033[93m'
        BRIGHT_BLUE = '\033[94m'
        BRIGHT_MAGENTA = '\033[95m'
        BRIGHT_CYAN = '\033[96m'
        BRIGHT_WHITE = '\033[97m'
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        UNDERLINE = '\033[4m'
        RESET = '\033[0m'

        @classmethod
        def get_color(cls, color_name):
            if color_name == 'BLACK':
                return cls.BLACK
            elif color_name == 'RED':
                return cls.RED
            elif color_name == 'GREEN':
                return cls.GREEN
            elif color_name == 'YELLOW':
                return cls.YELLOW
            elif color_name == 'UNDERLINE':
                return cls.UNDERLINE
            elif color_name == 'WHITE':
                return cls.WHITE
            elif color_name == 'CYAN':
                return cls.CYAN
            elif color_name == 'MAGENTA':
                return cls.MAGENTA
            elif color_name == 'BLUE':
                return cls.BLUE
            elif color_name == 'BRIGHT_WHITE':
                return cls.BRIGHT_WHITE
            elif color_name == 'BRIGHT_RED':
                return cls.BRIGHT_RED
            elif color_name == 'BRIGHT_GREEN':
                return cls.BRIGHT_GREEN
            elif color_name == 'BRIGHT_YELLOW':
                return cls.BRIGHT_YELLOW
            elif color_name == 'BRIGHT_BLUE':
                return cls.BRIGHT_BLUE
            elif color_name == 'BRIGHT_CYAN':
                return cls.BRIGHT_CYAN
            elif color_name == 'BRIGHT_WHITE':
                return cls.BRIGHT_WHITE
            elif color_name == 'BRIGHT_MAGENTA':
                return cls.BRIGHT_MAGENTA
            else:
                return cls.RESET
    @classmethod
    def rint(cls, s: str, color = 'BRIGHT_YELLOW',center=True, center_size=80, ch = ' ', end ='\n'):
        color = cls.COLOR.get_color(color)
        s_copy = s
        if center:
            s_copy = [s_copy[i:i+center_size].center(center_size,ch) for i in range(0, len(s_copy), center_size)]
        else:
            s_copy = [s_copy[i:i+center_size] for i in range(0, len(s_copy), center_size)]
        print(color,end='')
        for out in s_copy:
            print(out+end)
        print(cls.COLOR.RESET)
        

class time_chk:
    def __init__(self, s, DEBUG=1, rep_ch = '*', termsize = 60, color = 'BRIGHT_YELLOW'):
        self.__timeblock = s
        self.__entire_start=0
        self.__start = 0
        self.__end = 0
        self.__sec = 0
        self.__cnt = 0
        self.__DEBUG = DEBUG
        self.__isnew = 0
        self.__rep_ch = rep_ch
        self.__termsize = termsize
        self.__color = color

    def start(self):
        if self.__DEBUG == 0:
            return

        if self.__isnew == 0:
            self.__cnt = 0
            self.__isnew = 1
            self.__entire_start = time.time()
            self.__start = time.time()
            p.rint(self.__rep_ch*self.__termsize,color=self.__color, center_size=self.__termsize)
            p.rint((self.__timeblock),center_size=self.__termsize,color=self.__color)
        else:
            self.__isnew = 2
            self.__start = time.time()
        return self.__entire_start

    def end(self):
        if self.__DEBUG == 0:
            return
        if self.__isnew == 1:
            self.__end = time.time()
            self.__sec = self.__end-self.__start
            self.__sec = round(self.__sec,3)

            out = str(self.__cnt) + ' 걸린시간 : ' + str(datetime.timedelta(seconds=self.__sec))
            out += '  시작부터 '+ str(self.__end-self.__entire_start)[:5] +' s'

            p.rint(out,center_size=self.__termsize,color=self.__color)
        else:
            self.__end = time.time()
            self.__sec = self.__end-self.__start
            self.__sec = round(self.__sec,3)

            out = str(self.__cnt) + ' 걸린시간 : ' + str(datetime.timedelta(seconds=self.__sec))
            out += '  시작부터 '+ str(self.__end-self.__entire_start)[:5] +' s'

            p.rint(out,center_size=self.__termsize,color=self.__color)

        self.__cnt += 1
        return self.__timeblock

    def eend(self, entirestart, timeblock):
        if self.__DEBUG == 0:
            return
        self.__end = time.time()
        self.__sec = self.__end-entirestart
        self.__sec = round(self.__sec,3)
        p.rint(self.__rep_ch*self.__termsize,color=self.__color, center_size=self.__termsize)

        out = (timeblock+' 걸린시간 : '+str(datetime.timedelta(seconds=self.__sec))[:10])
        out += '  시작부터 '+ str(self.__end-self.__entire_start)[:5] +' s'+'\t 총 '+str(self.__sec)+'s'
    
        p.rint(out,center_size=self.__termsize,color=self.__color)
    
    def cut(self, timeblock=''):
        p.rint('\n'+str(self.__cnt)+' '+timeblock,center_size=self.__termsize,color=self.__color)
        self.end()
        self.start()
    
