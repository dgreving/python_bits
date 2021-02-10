from functools import update_wrapper


class record_calls:
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        return self.func(*args, **kwargs)


if __name__ == '__main__':
    #@record_calls
    def my_test_func():
        """
        useless docstring...
        """
        return 42

    my_test_func()
    #print(my_test_func.call_count)
    print(str(my_test_func))
