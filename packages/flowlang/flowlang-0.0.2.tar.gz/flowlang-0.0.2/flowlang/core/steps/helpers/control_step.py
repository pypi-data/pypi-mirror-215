from ...models import LLModel
from ..base import Step


class ControlStep(Step):

    name = "control_step"
    description = "selects the required module for execution to solve the task"
    properties = dict(
        task=dict(
            type='string',
            description="input task to solve",
            required=True
        )
    )
    prompt = """
    Your task is to determine which of the steps you need to call at the current moment, based on the available data, previous steps results and the task. \
    If you think that the end result is achieved, then you must call a step called "end_step". \
    Ask for clarification if a user task is ambiguous.
    """

    def __init__(self, model: LLModel, steps: dict, steps_specs: list) -> None:
        super(ControlStep, self).__init__(model)
        self.steps = steps
        self.steps_specs = steps_specs

    @property
    def history(self) -> list:
        return self.model.history


    def __call__(self, task: str) -> str:
        response = self.model(content=self.prompt, input_text=task, functions=self.steps, functions_spec=self.steps_specs)
        return response
