
import unittest
import inspect
from career.iiterator import FunctionIterator


#@unittest.skip("showing class skipping")
class FunctionIteratorTestCase(unittest.TestCase):

    search_keywords = ['data analytics','data engineer']

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        fi = FunctionIterator(obj=self.search_keywords, func=callable_func, duration=10, sleepsecs=2)
        self.assertEqual(fi.idx, 0)
        self.assertEqual(fi.len, 2)
        self.assertTrue(fi.iterable)

    def test__handle_kwargs(self):
        fi = FunctionIterator(obj=self.search_keywords, func=callable_func, caller=inspect.currentframe(), p1='param1', p2='param2')
        self.assertTrue(fi.dbgon)
        self.assertEqual(len(fi.kwargs), 3)
        while fi.iterable:
            keys = fi.nextop()
            self.assertEqual(len(keys), 3)

    def test__nextop(self):
        fi = FunctionIterator(obj=self.search_keywords, func=callable_func)
        while fi.iterable:
            fi.nextop()

    def text__report(self):
        fi = FunctionIterator(obj=self.search_keywords, func=callable_func, exp_runtime=3600)
        while fi.iterable:
            fi.nextop()
        self.assertTrue(hasattr(fi, 'idx'))
        self.assertTrue(hasattr(fi, 'len'))
        self.assertTrue(hasattr(fi, 'start_dt'))
        self.assertTrue(hasattr(fi, 'exp_runtime'))
        self.assertTrue(hasattr(fi, 'callername'))


def callable_func(it_value, **kwargs):
    print(f"it_value : {it_value}")
    print(f"kwargs :")
    pp.pprint(kwargs)
    return list(kwargs)


def test():
    unittest.main()

# if __name__ == '__main__':
#     unittest.main()
