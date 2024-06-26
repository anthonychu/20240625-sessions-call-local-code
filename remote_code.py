def main():

    # whenever we want to call a function in the local app, we use the call_function function with yield
    # control is yielded back to the local code to execute the function, then it'll send the function's result
    # back to the remote code to continue execution
    x = yield call_function("add", 1, 1)
    print("x=",x)
    y = yield call_function("multiply", 6, 7)
    print("y=",y)
    z = yield call_function("add", 3, 5)
    print("z=",z)

    # loops work too
    for i in range(3):
        yield call_function("add", 5, i)

    # if statement
    if x > 0:
        yield call_function("reverse_string", "hello world")
    else:
        yield call_function("add", 20, 5)

    return [x, y, z]