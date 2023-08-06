from ..base import Step


class ValidationStep(Step):

    name = "validation_step"
    description = "verifies that the answer is correct according the given task"
    properties = dict(
        answer=dict(
            type='string',
            description="answer to the task",
            required=True
        ),
        task=dict(
            type='string',
            description="given task",
            required=True
        ),
        context=dict(
            type='string',
            description='task context',
            required=True
        )
    )
    prompt = """
    You must check that the answer is correct for the task according the context. \
    You must admit that there may be a little inaccuracies in the answer. You should still count this answer as correct.
    Print result only by following dict format: {"evaluation": <evaluation_result>, "explanation": <your explanation>} and nothing else. \
    If this answer is correct, then you should replace <evaluation_result> with the exact message "valid" in "" quotes and replace <your explanation> with empty "" quotes. \
    If this answer is not correct, then you must should replace <evaluation_result> with the exact message "invalid" in "" quotes and deduce why the answer is not relevant to the context and place it into <your explanation> in "" quotes. \
    Your <evaluation_result> if it is not empty must be no more than 50 words. \
    """

    def __call__(self, answer: str, task: str, context: str) -> str:
        input_text = str(dict(answer=answer, task=task, context=context))
        response = self.model(content=self.prompt, input_text=input_text)
        return response
