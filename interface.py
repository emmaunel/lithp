from error import UnimplementedFunctionError, EvalutionError


class Eval:
    def eval(self, environment, args=None):
        raise EvalutionError(environment, args, "Evaluation error")


class Egal:
    def __eq__(self, rhs):
        raise UnimplementedFunctionError("Function not yet implemented", rhs)
