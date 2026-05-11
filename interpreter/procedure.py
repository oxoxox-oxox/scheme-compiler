from environment import Environment


class Procedure:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        # create new env
        new_env = Environment(self.params, args, self.env)
        # get value of function in new environment
        from analyse import evaluation
        return evaluation(self.body, new_env)
