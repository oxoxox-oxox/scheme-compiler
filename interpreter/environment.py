class Environment:
    def __init__(self, params=None, args=None, outer=None):
        # list of name, list of value, parent environment
        self.data = {}
        self.outer = outer

        if params and args:
            for param, arg in zip(params, args):
                self.data[param] = arg

    def define(self, var, val):
        # define the variety
        self.data[var] = val
        return val

    def get(self, var):
        # get value
        if var in self.data:
            return self.data[var]
        elif self.outer:
            return self.outer.get(var)
        else:
            raise NameError('薛定谔的变量是无法被查找到的')

    def set(self, var, val):
        # change the val of variety
        if var in self.data:
            self.data[var] = val
        elif self.outer:
            self.outer.set(var, val)
        else:
            raise NameError('薛定谔的变量是无法被定义的')
