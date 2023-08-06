from utils import set_vta
import tvm

from pathlib import Path
import ctypes


def load_lib():
    """加载库，函数将被注册到 TVM"""
    # 作为全局加载，这样全局 extern symbol 对其他 dll 是可见的。
    curr_path = "./lib/libtvm_ext.so"
    lib = ctypes.CDLL(curr_path, ctypes.RTLD_GLOBAL)
    return lib


_LIB = load_lib()

myadd = tvm.get_global_func("myadd")
print(myadd(4, 5))