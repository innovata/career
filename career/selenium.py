
import time
import os
import inspect


def clicker(webelem, secs=1):
    try:
        webelem.click()
        time_sleeper(secs)
    except Exception as e:
        print(f"{'#'*60}\n{os.path.abspath(__file__)} | {inspect.stack()[0][3]}\n Exception : {e}")
        return False
    else:
        return True

def time_sleeper(secs):
    for i in range(secs):
        time.sleep(1)
        print(f"{inspect.stack()[0][3]} : {i+1}초")
