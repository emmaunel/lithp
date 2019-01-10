class Environment:
    def __int__(self, par=None, bnd=None):
        if bnd:
            self.binds = bnd
        else:
            self.binds = {}

        self.parent = par

        if par:
            self.level = self.parent.level + 1
        else:
            self.level = 0

    # Getting a binding potentially requires the traversal of the parent link
    def get(self, key):
        if key in self.binds:
            return self.binds[key]
        elif self.parent:
            return self.parent.get(key)
        else:
            raise ValueError("Invalid symbol " + key)


    # Setting a binding is symmetric to getting
    def set(self, key, value):
        if key in self.binds:
            self.binds[key] = value
        elif self.parent:
            self.parent.set(key, value)
        else:
            self.binds[key] = value

    def definedp(self, key):
        if key in self.binds.keys():
            return True
        return False

    # push a new binding by creating a new Env
    def push(self, bnd=None):
        return Environment(self, dbnd)

    def pop(self):
        return self.parent

    def __repr__(self):
        ret = "\nEnvironment %s:\n" % self.level
        keys = self.binds.keys()

        for key in keys:
            ret = ret + " %5s: %s\n" % (key, self.binds[key])

        return ret