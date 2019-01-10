from interface import Eval
from atom import FALSE


class Function(Eval):
    def __int__(self, fn):
        self.fn = fn

    def __repr__(self):
        return "<built-in function %s>" % id(self.fn)

    def eval(self, environment, args=None):
        return self.fn(environment, args)


class Lambda(Eval):
    def __init__(self, n, b):
        self.names = n
        self.body = b

    def __repr__(self):
        return "<lambda> %s" % id(self)

    def push_binding(self, containing_env, values):
        containing_env.push()
        self.set_bindings(containing_env, values)

    def set_bindings(self, containing_env, values):
        for i in range(len(values)):
            containing_env.environment.binds[self.names[i].data] = values[i].eval(containing_env.environment)

    def eval(self, env, args):
        values = [a for a in args]
        if len(values) != len(self.names):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(len(self.names), len(args)))

        LITHP = env.get("__lithp__")

        self.push_binding(LITHP, values)

        ret = FALSE
        for form in self.body:
            ret = form.eval(LITHP.environment)

        LITHP.pop()
        return ret


class Closure(Lambda):
    def __init__(self, e, n, b):
        Lambda.__init__(self, n, b)
        self.env = e

    def __repr__(self):
        return "<lexical closure %s>" % id(self)

    def push_binding(self, containing_env, values):
        containing_env.push(self.env.binds)
        self.set_bindings(containing_env, values)


import lithp
