import inspect
import os
import sys

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
sys.path.append(real_path)

try:
    import zeroset.cv0 as cv0
except ImportError as e:
    print(e, "Import Error")
    exit(1)

__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]
