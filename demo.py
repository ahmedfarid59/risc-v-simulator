import functions
import sys
import inspect

function_names = [func for func, _ in inspect.getmembers(sys.modules["functions"], inspect.isfunction)]
print(function_names)
