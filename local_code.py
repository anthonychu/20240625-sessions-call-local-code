import json
import os
from azure_container_apps import DynamicSessionsClient


def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def reverse_string(s):
    return s[::-1]

local_functions = {
    "add": add,
    "multiply": multiply,
    "reverse_string": reverse_string,
}

client = DynamicSessionsClient(os.getenv("POOL_MANAGEMENT_ENDPOINT"))

# Load some libs needed in the remote session
session_libs_code = open("session_libs.py", "r").read()
client.execute(session_libs_code)


# Load the code to run in the remote session
main_code = open("remote_code.py", "r").read()
client.execute(main_code)


# The following code runs the main code using the orchestrator (couldn't think of a better name 
# for this so I named it after the Durable Functions thing) and executes local functions when
# the main code calls them.
execute_code = "o = Orchestrator(main())"
code_exec_result = client.execute(execute_code)

next_input = json.dumps(None)
while True:
    # next_input is already a json string, double encode it
    code = 'o.run_to_next(%s)' % json.dumps(next_input)
    code_exec_result = client.execute(code)
        
    result = json.loads(code_exec_result["result"])
    print(result)

    if result["result_type"] == "function_call":
        func = local_functions[result["function_name"]]
        print(f"Local function call: {result['function_name']} {result['args']}")
        result = func(*result["args"])
        print(f"Local function call result: {result}")
        next_input = json.dumps(result)
    elif result["result_type"] == "return_value":
        print(f'Result: {result["return_value"]}')
        break