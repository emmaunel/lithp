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
            self.stdout.write( "%s " % str(result))

        self.stdout.write("\n")
        return TRUE

    def cond(self, env, args):
        pass