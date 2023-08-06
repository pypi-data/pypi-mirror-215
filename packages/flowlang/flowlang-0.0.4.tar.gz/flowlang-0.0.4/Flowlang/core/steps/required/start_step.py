from ..base import Step


class StartStep(Step):

    name = "start_step"
    description = "starting scenario flow"
    properties = dict(
        task=dict(
            type='string',
            description="input text",
            required=True
        )
    )
    prompt = """"""

    def __call__(self, task: str) -> str:
        return task
