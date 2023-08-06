from ..base import Step


class SummarizationStep(Step):

    name = "summarization_step"
    description = "summarize the input text"
    properties = dict(
        text=dict(
            type='string',
            description="input text to summarize",
            required=True
        ),
        action=dict(
            type='string',
            enum=['summarize', 'describe', 'extract main information from'],
            required=True
        ),
        words_limitation=dict(
            type='integer',
            description="maximum words in summary"
        )
    )
    prompt = """
    Your task is to {action} the text. \
    {words_limitation}
    """

    def __call__(self, text: str, action: str, words_limitation=None) -> str:
        prompt = self.prompt
        if words_limitation:
            prompt = prompt.replace('{words_limitation}', f'Do it in at most {words_limitation} words.')
        prompt = prompt.replace('{action}', action)
        response = self.model(content=prompt, input_text=text)
        return response
