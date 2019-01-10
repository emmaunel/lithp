import pdb
import getopt, sys, io
from env import Environment
from fun import Function
from atom import TRUE
from atom import FALSE
from lisp import Lisp
from reader import Reader
from error import Error
from fun import Lambda
from fun import Closure

NAME = "Lithp"
VERSION = "v1.1"
PROMPT = "lithp"
DEPTH_MARK = "."


class Lithp(Lisp):
    def __init__(self):
        iostreams = sys.stdin, sys.stdout, sys.stderr
        (self.stdin, self.stdout, self.stderr) = iostreams

        self.debug = False
        self.verbose = True
        self.core = True
        self.closures = True

        self.rdr = Reader()
        self.environment = Environment()

        self.init()

    def init(self):
        self.environment.set("eq", Function(self.eq))
        self.environment.set("quote", Function(self.quote))
        self.environment.set("car", Function(self.car))
        self.environment.set("cdr", Function(self.cdr))
        self.environment.set("cons", Function(self.cons))
        self.environment.set("atom", Function(self.atom))
        self.environment.set("cond", Function(self.cond))

        self.environment.set("print", Function(self.println))

        self.environment.set("lambda", Function(self.lambda_))
        self.environment.set("label", Function(self.label))

        self.environment.set("t", TRUE)

        self.environment.set("nil", FALSE)

        self.environment.set("__lithp__", self)
        self.environment.set("__global__", self.environment)


    def usage(self):
        self.print_banner()
        print()
        print(NAME.lower(), " <options> [lithp files]\n")


    def print_banner(self):
        print("The", NAME, "programming shell", VERSION)
        print("  Type :help for more information")
        print()

    def print_help(self):
        print("Help for Lithp v", VERSION)
        print("  Type :help for more information")
        print("  Type :env to see the bindings in the current environment")
        print("  Type :load followed by one or more filenames to load source files")
        print("  Type :quit to exit the interpreter")

    def push(self, env=None):
        if env:
            self.environment = self.environment.push(env)
        else:
            self.environment = self.environment.push()

    def pop(self):
        self.environment = self.environment.pop()

    def repl(self):
        while True:
            source = self.get_complete_command()

            if source in [":quit"]:
                break
            elif source in [":help"]:
                self.print_help()
            elif source.startswith(":load"):
                files = source.split(" ")[1:]
                self.process_files(files)
            elif source in [":env"]:
                print(self.environment)
            else:
                self.process(source)

    def process(self, source):
        sexpr = self.rdr.get_sexpr(source)
        while sexpr:
            result = None

            try:
                result = self.eval(sexpr)
            except Error as err:
                print(err)

            if self.verbose:
                self.stdout.write("   %s\n" % result)

            sexpr = self.rdr.get_sexpr()

    def lambda_(self, env, args):
        if self.environment != env.get("__global__") and self.closures:
            return Closure(env, args[0], args[1:])
        else:
            return Lambda(args[0], args[1:])

    def eval(self, sexpr):
        try:
            return sexpr.eval(self.environment)
        except ValueError as err:
            print(err)
            return FALSE

    def get_complete_command(self, line="", depth=0):
        if line != "":
            line = line + " "

        if self.environment.level != 0:
            prompt = PROMPT + " %i%s " % (self.environment.level, DEPTH_MARK * (depth+1))
        else:
            if depth == 0:
                prompt = PROMPT + "> "
            else:
                prompt = PROMPT + "%s " % (DEPTH_MARK * (depth+1))

            line = line + self.read_line(prompt)

            balance = 0
            for ch in line:
                if ch == "(":
                    balance = balance + 1
                elif ch == ")":
                    balance = balance - 1

            if balance > 0:
                return self.get_complete_command(line, depth+1)
            elif balance < 0:
                raise ValueError("Invalid parent pattern")
            else:
                return line

    def read_line(self, prompt):
        if prompt and self.verbose:
            self.stdout.write("%s" % prompt)
            self.stdout.flush()

        line = self.stdin.readline()

        if len(line) == 0:
            return "EOF"

        if line[-1] == "\n":
            line = line[:-1]

        return line

    def process_files(self, files):
        self.verbose = False

        for filename in files:
            infile = open(filename, 'r')
            self.stdin = infile

            source = self.get_complete_command()
            while(source not in ["EOF"]):
                self.process(source)

                source = self.get_complete_command()

            infile.close()
        self.stdin = sys.stdin
        self.verbose = True


if __name__ == '__main__':
    lithp = Lithp()

    try:
        opts, files = getopt.getopt(sys.argv[1:], "hd", ["help", "debug", "no-core", "no-closures"])
    except getopt.GetoptError as err:
        print(str(err))
        lithp.usage()
        sys.exit(1)

    for opt, arg in opts:
        pass