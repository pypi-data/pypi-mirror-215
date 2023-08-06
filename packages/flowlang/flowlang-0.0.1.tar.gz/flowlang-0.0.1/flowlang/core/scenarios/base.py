from enum import Enum
from ..steps import ControlStep
import ast


class ScenarioMode(Enum):

    AUTO = 0
    DEFINED = 1


class Scenario(object):

    def __init__(self) -> None:
        self.steps = dict()
        self.steps_specs = list()
        self.control_step = None
        
    def setup(self, steps: list, needs_control=False, control_model=None):
        self.steps = {step.name: step for step in steps}
        self.steps_specs = [step.spec for step in steps]
        if needs_control:
            self.control_step = ControlStep(control_model, self.steps, self.steps_specs)


    def run(self, task: str, mode: ScenarioMode, flow=None, max_attempts=10):
        scenario_run = ScenarioRun(self, task=task, mode=mode, flow=flow, control_step=self.control_step, max_attempts=max_attempts)
        return scenario_run.execute()



class ScenarioRun:


    def __init__(self, scenario: Scenario, **run_params) -> None:
        self.scenario = scenario
        self.__dict__.update(**run_params)
        self.__execute_switch = {
            ScenarioMode.AUTO: self.run_auto,
            ScenarioMode.DEFINED: self.run_static
        }
        self._history = dict()
        self.result = None

    @property
    def history(self) -> dict:
        return dict(sorted(self._history.items(), key=lambda item: item[1]['id']))

    def execute(self):
        return self.__execute_switch[self.mode]()

    def run_auto(self):
        self._history['task'] = {'data': self.task, 'id': 0}
        task = self.task
        is_end = False
        attempt = 0
        while not is_end:
            attempt += 1
            print(f"Task: {task}")
            response = self.control_step(task)['result']
            task = response
            func_call = self.control_step.history[-1].get('function_call')
            if func_call:
                func_call = ast.literal_eval(func_call)
                print(f"Func call: {func_call}")
                self._history[func_call.get('name', 'unknown')] = {'data': response, 'id': attempt}
                if func_call.get('name') == 'end_step':
                    is_end = True
            else:
                self._history['control'] = {'data': response, 'id': attempt}
            if attempt == self.max_attempts:
                is_end = True
        if self._history.get("end_step"):
            self.result = self._history["end_step"]['data']
        else:
            self.result = "Max attempts achieved."
        return self


    def run_static(self):
        self._history['task'] = {'data': self.task, 'id': 0}
        for i, flow_step in enumerate(self.flow):
            step_inputs = dict()
            for arg_name, arg_value in flow_step["inputs"].items():
                step_inputs[arg_name] = self._history[arg_value[1:]]['data'] if "$" in arg_value else arg_value
            step = self.scenario.steps[flow_step["name"]]
            response = step(**step_inputs)
            self._history[flow_step["name"]] = {'data': response, 'id': i+1}
        self.result = self._history["end_step"]['data']
        return self
