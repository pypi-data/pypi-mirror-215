from ...models import LLModel
from ..base import Step


class ApiCallStep(Step):

    name = "api_call_step"
    description = "gives the necessary api request to the service to solve the task"
    properties = dict(
        task=dict(
            type='string',
            description="input task to solve with api request",
            required=True
        )
    )
    prompt = """
    Ask for clarification if a user task is ambiguous.
    """

    def __init__(self, model: LLModel, endpoints: dict, endpoints_specs: list) -> None:
        super(ApiCallStep, self).__init__(model)
        self.endpoints = endpoints
        self.endpoints_specs = endpoints_specs

    @property
    def history(self) -> list:
        return self.model.history


    def __call__(self, task: str) -> str:
        response = self.model(content=self.prompt, input_text=task, functions=self.endpoints, functions_spec=self.endpoints_specs)
        return response
