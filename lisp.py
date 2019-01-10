from atom import TRUE
from atom import FALSE
from atom import Symbol
from seq import Seq
from fun import Lambda


class Lisp:
    SPECIAL = "()"

    def dummy(self, env, args):
        print("I do nothing, but you gave me: ")
        self.println(env, args)

    def println(self, env, args):
        for a in args:
            result = a.eval(env)
            self.stdout.write("%s " % str(result))

        self.stdout.write("\n")
        return TRUE

    def cond(self, env, args):
        for test in args:
            result = test.car().eval(env)

            if result == TRUE:
                return test.data[1].eval(env)

        return FALSE

    def eq(self, env, args):
        if len(args) > 2:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        if args[0].eval(env) == args[1].eval(env):
            return TRUE

        return FALSE

    def quote(self, env, args):
        if len(args) > 1:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        return args[0]

    def car(self, env, args):
        if len(args) > 1:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        cell = args[0].eval(env)

        if not isinstance(cell, Seq):
            raise ValueError("Function not valid on non-sequence type.")

        return cell.car()

    def cdr(self, env, args):
        if len(args) > 1:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        cell = args[0].eval(env)

        if not isinstance(cell, Seq):
            raise ValueError("Function not valid on non-sequence type.")
        return cell.cdr()

    def cons(self, env, args):
        if len(args) > 2:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        first = args[0].eval(env)
        second = args[1].eval(env)

        return second.cons(first)

    def atom(self, env, args):
        if len(args) > 1:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        first = args[0].eval(env)

        if first == FALSE:
            return TRUE
        elif isinstance(first, Symbol):
            return TRUE

        return FALSE

    def label(self, env, args):
        if len(args) != 2:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        env.set(args[0].data, args[1].eval(env))
        return env.get(args[0].data)
