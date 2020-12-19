import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
#logging.disable(logging.FATAL)
tests_enable = True

def left_to_right_eval(args_n_ops):
    logging.debug("left to right eval: %s", args_n_ops)
    result = int(args_n_ops.pop(0))
    while args_n_ops:
        op = args_n_ops.pop(0)
        arg = int(args_n_ops.pop(0))
        if op == "+":
            result += arg
        elif op == "*":
            result *= arg
    logging.debug("result: %d" % result)
    return result

def allmighty_plus_eval(args_n_ops):
    logging.debug("allmighty plus eval: %s", args_n_ops)
    #deal with pluses first, then we can do left_to_right
    while "+" in args_n_ops:
        plus_idx = args_n_ops.index("+")
        tmp_eval = [args_n_ops.pop(plus_idx - 1), #arg1
                    args_n_ops.pop(plus_idx - 1), #op
                    args_n_ops.pop(plus_idx - 1)] #arg2
        args_n_ops.insert(plus_idx - 1, str(left_to_right_eval(tmp_eval)))
    return left_to_right_eval(args_n_ops)

# expr is a string
def evaluate(expr, eval_func):
    logging.debug("evaluating expr: '%s'" % expr)
    while "(" in expr:
        sub_end = expr.find(")")
        sub_start = sub_end
        while expr[sub_start] != "(":
            sub_start -= 1
        sub_expr = evaluate(expr[sub_start+1:sub_end], eval_func)
        expr = "".join((expr[:sub_start], sub_expr, expr[sub_end+1:]))
        logging.debug("new expr: '%s'" % expr)
    args_n_ops = expr.split()
    result = eval_func(args_n_ops)
    return str(result)

if tests_enable:
    test_ins = []
    with open("test_inputs", "r") as f:
        for line in f:
            test_ins.append(line.rstrip())
    test_outs = []
    with open("test_outputs", "r") as f:
        for line in f:
            test_outs.append(line.rstrip())
    for test in zip(test_ins, test_outs):
        test_in, test_out = test
        assert(evaluate(test_in, left_to_right_eval) == test_out)
    test_outs = []
    with open("test_outputs2", "r") as f:
        for line in f:
            test_outs.append(line.rstrip())
    for test in zip(test_ins, test_outs):
        test_in, test_out = test
        assert(evaluate(test_in, allmighty_plus_eval) == test_out)

actual_in = []  
with open("input", "r") as f:
    for line in f:
        actual_in.append(line.rstrip())
print(sum(map(lambda x: int(evaluate(x, left_to_right_eval)), actual_in)))
print(sum(map(lambda x: int(evaluate(x, allmighty_plus_eval)), actual_in)))
