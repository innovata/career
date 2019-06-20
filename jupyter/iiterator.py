
from jupyter.hydrogen import *
#============================================================ Project
from career.iiterator import *
from career import iiterator

#============================================================
"""Initialize. | Reload."""
#============================================================

search_keywords = [
    'data analytics',
    'data engineer',
    'machine learning',
    'python'
    'business intelligence (bi)',
    'data analysis',
    'Data Scientist',
    'Artificial Intelligence (AI)',
    'natural language processing',
    'Node.js']


importlib.reload(iiterator)
FunctionIterator = iiterator.FunctionIterator

#============================================================
"""Excuter."""
#============================================================

def callable_func(it_value, **kwargs):
    print(f"it_value : {it_value}")
    print(f"kwargs :")
    pp.pprint(kwargs)

fi = FunctionIterator(obj=search_keywords, func=callable_func, avg_runtime=1, p1='param1',p2='param2')
fi.__dict__


def calling_func():
    fi = FunctionIterator(obj=search_keywords, func=callable_func, avg_runtime=1, p1='param1',p2='param2',caller=inspect.currentframe())
    while fi.iterable:
        fi.nextop()

calling_func()
