cdef extern from "ola.h":
    cdef void say_hello()


def ola():
    say_hello()
