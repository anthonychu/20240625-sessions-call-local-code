# Example showing how to use generators to call local functions from a remote session

Code execution in Azure Container Apps dynamic sessions' code interpreter API is one-way only, where the local app can send code to the remote session for execution, but the remote session cannot call back into the local app. This limitation can be overcome by using generators to call local functions from a remote session.

This example demonstrates how to use generators to call local functions from a remote session. The example consists of two key files:

* [`remote_code.py`](./remote_code.py): Contains the code that will be executed in the remote session. It's a generator function called `main` that yields code to be executed in the local app.
* [`local_code.py`](./local_code.py): Contains the local functions that the remote session will call.

To run the example:

1. Create a `.env` file and add a `POOL_MANAGEMENT_ENDPOINT` environment variable with the value of the Azure Container Apps Python code interpreter session pool management endpoint.
1. `poetry install`
1. `poetry run python local_code.py`

It should output result like below:

```
{'result_type': 'function_call', 'function_name': 'add', 'args': [1, 1]}
Local function call: add [1, 1]
Local function call result: 2
{'result_type': 'function_call', 'function_name': 'multiply', 'args': [6, 7]}
Local function call: multiply [6, 7]
Local function call result: 42
{'result_type': 'function_call', 'function_name': 'add', 'args': [3, 5]}
Local function call: add [3, 5]
Local function call result: 8
{'result_type': 'function_call', 'function_name': 'add', 'args': [5, 0]}
Local function call: add [5, 0]
Local function call result: 5
{'result_type': 'function_call', 'function_name': 'add', 'args': [5, 1]}
Local function call: add [5, 1]
Local function call result: 6
{'result_type': 'function_call', 'function_name': 'add', 'args': [5, 2]}
Local function call: add [5, 2]
Local function call result: 7
{'result_type': 'function_call', 'function_name': 'reverse_string', 'args': ['hello world']}
Local function call: reverse_string ['hello world']
Local function call result: dlrow olleh
{'result_type': 'return_value', 'return_value': [2, 42, 8]}
Result: [2, 42, 8]
```