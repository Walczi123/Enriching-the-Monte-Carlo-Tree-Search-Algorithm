class A(object):
    def fun(self):
        print("asdada")

def f(function):
    function()

a = A()
f(a.fun)