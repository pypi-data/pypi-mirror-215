from ..base import Step


class EndStep(Step):

    name = "end_step"
    description = "ending scenario flow"
    properties = dict(
        result=dict(
            type='string',
            description="input text",
            required=True
        )
    )
    prompt = """"""

    def __call__(self, result: str) -> str:
        return result
