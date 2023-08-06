from ..base import Step


class TranslationStep(Step):

    name = "translation_step"
    description = "translate the input text from one language to another"
    properties = dict(
        text=dict(
            type='string',
            description="input text to translate",
            required=True
        ),
        from_language=dict(
            type='string',
            description="the language from which the text needs to be translated",
            required=True
        ),
        to_language=dict(
            type='string',
            description="the language into which the text needs to be translated",
            required=True
        ),
        style=dict(
            type='string',
            description="translation style",
            required=True
        )
    )
    prompt = """
    Your task is to translate the text from {from_language} to {to_language} in {style} style. \
    You must keep all special characters in the text like: "<", ">", "{", "}", "[", "]".
    """

    def __call__(self, text: str, from_language: str, to_language: str, style: str) -> str:
        prompt = self.prompt
        prompt = prompt.replace('{from_language}', from_language).replace('{to_language}', to_language)
        prompt = prompt.replace('{style}', style)
        response = self.model(content=prompt, input_text=text)
        return response
