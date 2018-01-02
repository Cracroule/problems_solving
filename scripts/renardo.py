import datetime as dt

"""renardo.py: 'Des chiffres et des lettres' solving """
__author__ = "Raoul Pillard"


def main():
    t1 = dt.datetime.now()

    input_numbers = [5, 8, 4, 6, 7, 2]
    target_number = 668

    print('input', input_numbers)
    print('target', target_number)
    print('')

    sorted_numbers = [TraceableInteger(e) for e in sorted(input_numbers)]
    universe_of_solution, solution = find_universe_of_results(tuple(sorted_numbers), target_number)

    if solution:
        print("solution found !")
        print(solution.history, '=', solution.value)
    else:
        print("There is no solution for this problem")

    t2 = dt.datetime.now()
    print('')
    print("computed in ", (t2 - t1).total_seconds(), "seconds")


def memoize(function):
    from functools import wraps

    memo = {}

    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper


class TraceableInteger(object):

    def __init__(self, value, history=None):
        self.value = int(value)
        self.history = history
        if not history:
            self.history = str(int(value))

    def __str__(self):
        return str(self.value)

    def __lt__(self, other):
        return self.value < other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __hash__(self):
        return hash(self.value)

    @staticmethod
    def apply_operator(t_a, t_b, op):
        a = int(t_a.value)
        b = int(t_b.value)
        if op == '+':
            value = a+b
        elif op == '-':
            value = a-b
        elif op == '*':
            value = a*b
        elif op == '/':
            value = a/b
        else:
            raise Exception("please use only allowed operators")
        return TraceableInteger(value, '(' + t_a.history + op + t_b.history + ')')


# compute all integer results from a, b and operators (+, -, * and /)
def apply_all_operators(t_a, t_b):
    trivial_res = [t_a, t_b]
    res = [TraceableInteger.apply_operator(t_a, t_b, '+'), TraceableInteger.apply_operator(t_a, t_b, '*')]
    if t_a.value > t_b.value:
        res.append(TraceableInteger.apply_operator(t_a, t_b, '-'))
        if t_b.value and (not t_a.value % t_b.value):
            res.append(TraceableInteger.apply_operator(t_a, t_b, '/'))
    elif t_a.value < t_b.value:
        res.append(TraceableInteger.apply_operator(t_b, t_a, '-'))
        if t_a.value and (not t_b.value % t_a.value):
            res.append(TraceableInteger.apply_operator(t_b, t_a, '/'))
    elif t_a and t_b:  # equality case
        res.append(TraceableInteger.apply_operator(t_a, t_b, '/'))
    return trivial_res + res


def extract_all_pairs(input_tuple):
    res = list()
    for i, el_i in enumerate(input_tuple):
        for j, el_j in enumerate(input_tuple):
            if i != j:
                remaining_elements = list(input_tuple)
                remaining_elements.remove(el_i)
                remaining_elements.remove(el_j)
                res.append((el_i, el_j, tuple(remaining_elements)))
    return res


@memoize
def generate_all_results_from_pair(input_tuple):
    res = list()
    paired_universe = extract_all_pairs(input_tuple)
    for el_i, el_j, remaining_tuple in paired_universe:
        generated_from_pair = apply_all_operators(el_i, el_j)
        for t_r in generated_from_pair:
            res.append(tuple(sorted(remaining_tuple + (t_r,))))
    return res


def find_universe_of_results(input_tuple, target=None):
    universe_of_res = list()
    found_solution = None

    def expand_res_universe(my_tuple, stop_target):
        new_universe_of_results = set(generate_all_results_from_pair(my_tuple))
        for cur_tuple in new_universe_of_results:
            if len(cur_tuple) > 1:
                expand_res_universe(cur_tuple, stop_target)
            else:
                universe_of_res.append(cur_tuple[0])
                if cur_tuple[0].value == stop_target:
                    raise ValueError  # dirty way to stop computations if solution is found
    try:
        expand_res_universe(input_tuple, target)
    except ValueError:
        found_solution = universe_of_res[-1]  # a solution has been found
    return universe_of_res, found_solution


if __name__ == '__main__':
    main()
