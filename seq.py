from interface import Eval, Egal
from error import UnimplementedFunctionError


class Seq(Eval, Egal):
    def __init__(self):
        self.data = None

    def car(self):
        return self.data[0]

    def cdr(self):
        raise UnimplementedFunctionError("Function not yet implemented for ", self.__class__.__name__)

    def cons(self, e):
        raise UnimplementedFunctionError("Function not yet implemented for ", self.__class__.__name__)

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data

    def __getitem__(self, item):
        return self.data[item]

    def __eq__(self, other):
        if not isinstance(other, Seq):
            return False

        if len(self) != len(other):
            return False

        for i in range(len(self.data)):
            if not self.data[i] == other.data[i]:
                return False

        return True


class List(Seq):
    def __init__(self, l=None):
        Seq.__init__(self)

        if l is None:
            self.data = []
        else:
            self.data = l

    def cdr(self):
        try:
            return List(self.data[1:])
        except:
            return List([])

    def cons(self, e):
        ret = List(self.data[:])
        ret.data.insert(0, e)
        return ret

    def eval(self, environment, args=None):
        form = self.car().eval(environment)
        return form.eval(environment, self.cdr())

    def __repr__(self):
        if self.data == []:
            return "()"

        ret = "(%s" % self.data[0]
        for e in self.data[1:]:
            ret = ret + " %s" % e

        return ret + ")"
