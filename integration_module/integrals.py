import ctypes
from pathlib import Path

LIBRARY_PATH = (
    Path(__file__).resolve().parent
    / "build"
    / "libintegrals.dll"
)

lib = ctypes.CDLL(str(LIBRARY_PATH))

Function = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)

lib.left_rectangle_integral.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    Function,
    ctypes.c_int
]
lib.left_rectangle_integral.restype = ctypes.c_double

lib.right_rectangle_integral.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    Function,
    ctypes.c_int
]
lib.right_rectangle_integral.restype = ctypes.c_double

lib.middle_rectangle_integral.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    Function,
    ctypes.c_int
]
lib.middle_rectangle_integral.restype = ctypes.c_double

lib.trapezoid_integral.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    Function,
    ctypes.c_int
]
lib.trapezoid_integral.restype = ctypes.c_double

lib.simpson_integral.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    Function,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int)
]
lib.simpson_integral.restype = ctypes.c_double

lib.monte_carlo_integrals.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    Function,
    ctypes.c_longlong,
]
lib.monte_carlo_integrals.restype = ctypes.c_double

lib.initialize_random.argtypes = []
lib.initialize_random.restype = None

lib.initialize_random()


c_func = Function(("func", lib))


def left_rectangle(a, b, n):
    return lib.left_rectangle_integral(a, b, c_func, n)

def right_rectangle(a, b, n):
    return lib.right_rectangle_integral(a, b, c_func, n)

def middle_rectangle(a, b, n):
    return lib.middle_rectangle_integral(a, b, c_func, n)

def trapezoid(a, b, n):
    return lib.trapezoid_integral(a, b, c_func, n)

def simpson(a, b, n):
    code = ctypes.c_int(0)
    res = lib.simpson_integral(a, b, c_func, n, ctypes.byref(code))
    if code.value != 0:
        raise ValueError("Для метода Симпсона n должно быть чётным")
    return res

def monte_carlo(a, b, n):
    return lib.monte_carlo_integrals(a, b, c_func, n)