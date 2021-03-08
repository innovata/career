
#============================================================ Python
import sys
import time
from datetime import datetime
import inspect
#============================================================ Etc.
import pandas as pd
from ilib import inumber


#============================================================

#============================================================

class FunctionIterator:
    """Additional **kwargs description.
    caller : inspect.currentframe() --> caller 입력하면 자동으로 로그를 찍는다.
    exp_runtime : expected runtime [secs]
    """

    def __init__(self, obj, func, exp_runtime=600, **kwargs):
        self.obj = obj
        self.it = iter(obj)
        self.idx = 0
        self.len = len(obj)
        self.iterable = True
        self.func = func
        self.kwargs = kwargs
        self.start_dt = datetime.now().astimezone()
        self.exp_runtime = exp_runtime
        self._handle_kwargs()

    def nextop(self):
        # print(f"{'-'*60}\n pre-iterable : {self.iterable}")
        # if self.iterable:
        try:
            # print(f"next(self.it) : {next(self.it)}")
            self.func(next(self.it), **self.kwargs)
        except Exception as e:
            self.iterable = False
            print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n StopIteration. self.iterable : {self.iterable}")
        else:
            self.iterable = True
            self.idx += 1
            self.report_loop()

    def _handle_kwargs(self):
        if 'caller' in list(self.kwargs):
            self.dbgon = True
            frameinfo = inspect.getframeinfo(frame=self.kwargs['caller'])
            self.callername = frameinfo.function
        else:
            self.dbgon= False

    def report_loop(self):
        cum_runtime = (datetime.now().astimezone() - self.start_dt).total_seconds()
        avg_runtime = cum_runtime / (self.idx)
        leftover_runtime = avg_runtime * (self.len - self.idx)
        if self.dbgon:
            print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]} : {self.idx}/{self.len}")
            print(f"callername : {self.callername}")
            tpls = [
                ('누적실행시간', cum_runtime),
                ('잔여실행시간', leftover_runtime),
                ('평균실행시간', avg_runtime),
            ]
            for tpl in tpls:
                timeexp, unit = inumber.convert_timeunit(tpl[1])
                print(f" {tpl[0]} : {timeexp} ({unit})")
        if self.len == self.idx:
            if (self.exp_runtime is not None) and (avg_runtime > self.exp_runtime):
                print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n Save the final report into DB.")
