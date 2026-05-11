import re
from functools import reduce
from environment import Environment
from procedure import Procedure


def tokenize(s: str) -> str:
    """transfer Scheme string into token list"""
    return re.findall(r'''"(?:[^"\\]|\\.)*"|\(|\)|'|`|[^\s()'`"]+''', s)


def parse(token: str) -> list:
    """read the expression from the token list"""
    token_list = list(token)

    def read_from(token_list: list) -> list:
        t = token_list.pop(0)

        if t == '(':
            # start to read list
            result = []
            while token_list and token_list[0] != ')':
                result.append(read_from(token_list))
            token_list.pop(0)
            return result

        elif t == ')':
            raise SyntaxError("那我问你，为什么这里会有一个')'?")

        elif t == "'":
            # deal with quote
            return ['quote', read_from(token_list)]
        else:
            return atom(t)

    return read_from(token_list)


def atom(token: any) -> any:
    """transfer token into python object"""
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            return token


def evaluation(expr: any, env: Environment) -> any:
    if isinstance(expr, (int, float)):
        return expr

    if isinstance(expr, str):
        return env.get(expr)  # 从环境查找符号

    if not isinstance(expr, list):
        return expr
    else:
        if expr[0] == 'if':
            test = evaluation(expr[1], env)
            if test:
                return evaluation(expr[2], env)
            else:
                return evaluation(expr[3], env)

        elif expr[0] == 'lambda':
            params = expr[1]
            body = expr[2]
            return Procedure(params, body, env)

        elif expr[0] == 'define':
            var = expr[1]

            if isinstance(var, list):
                func_name = var[0]
                params = var[1:]
                body = expr[2]
                proc = Procedure(params, body, env)
                env.define(func_name, proc)
                return func_name

            else:
                value = evaluation(expr[2], env)
                env.define(var, value)
                return var

        elif expr[0] == 'quote':
            return expr[1]

        else:
            func = evaluation(expr[0], env)
            args = [evaluation(arg, env) for arg in expr[1:]]
            return func(*args)


def create_global_env():
    env = Environment()
    env.define('+', lambda *args: sum(args))
    env.define('-', lambda a, *args: a - sum(args))
    env.define('*', lambda *args: reduce(lambda x, y: x * y, args, 1))
    env.define('/', lambda a, b: a / b)
    env.define('>', lambda a, b: a > b)
    env.define('<', lambda a, b: a < b)
    env.define('=', lambda a, b: a == b)
    # add more operation here

    return env


def repl():
    env = create_global_env()

    while True:
        try:
            code = input(">>> ")
            if code == "(quit)":
                break
            tokens = tokenize(code)
            expr = parse(tokens)
            result = evaluation(expr, env)
            print(result)
        except Exception as e:
            print(f'Error: {e}')


if __name__ == "__main__":
    repl()
