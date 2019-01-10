class Error(Exception):
    pass


class UnimplementedFunctionError(Error):
    def __init__(self, message, thing):
        self.thing = thing
        self.message = message

    def __str__(self):
        return self.message + repr(self.thing)


class EvalutionError(Error):
    def __int__(self, env, args, message):
        self.env = env
        self.args = args
        self.message = message

    def __str__(self):
        return self.message + ", " + repr(self.args) + " in environment " + self.env.level
