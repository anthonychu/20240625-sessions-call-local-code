import json


class Orchestrator:

    def __init__(self, generator):
        self.generator = generator

    def run_to_next(self, send_value=None):
        try:
            send_value = json.loads(send_value)
            next_val = self.generator.send(send_value)
            return json.dumps({
                "result_type": "function_call",
                "function_name": next_val.function_name,
                "args": next_val.args
            })
        except StopIteration as e:
            return json.dumps({
                "result_type": "return_value",
                "return_value": e.value
            })


class FunctionCall:
    def __init__(self, function_name, *args):
        self.function_name = function_name
        self.args = args


def call_function(function_name, *args):
    return FunctionCall(function_name, *args)
