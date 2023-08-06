from .base import LLModel
import openai
import json


class OpenAIModel(LLModel):

    def __init__(self, model_name: str, openai_token: str, history_volume=0, **model_params) -> None:
        super(OpenAIModel, self).__init__()
        openai.api_key = openai_token
        self.model_name = model_name
        self.model_params = model_params
        self._history_volume = history_volume
        self.history = []
    
    def __call__(self, content: str, input_text: str, functions=None, functions_spec=None) -> str:
        if functions:
            response = self._functions(content, input_text, functions=functions, functions_spec=functions_spec)
        else:
            response =  self._completion(content, input_text)
        return response
    
    def save_history(self, *messages):
        if self._history_volume == 0:
            return
        if len(self.history) >= self._history_volume:
            self.history = self.history[1:]
        for message in messages:
            self.history.append(message)
    
    def _completion(self, content: str, input_text: str) -> str:
        messages = [dict(role='system', content=content)]
        for hist in self.history:
            messages.append(dict(role=hist['role'], content=hist['content']))
        messages.append(dict(role='user', content=input_text))
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                **self.model_params
            ).get('choices')[0].get('message', dict()).get('content', "")
        except KeyError:
            response = "Key Error [0]. Do not have enough information."
        self.save_history(messages[-1], dict(role='assistant', content=response))
        return response

    def _functions(self, content: str, input_text: str, functions=None, functions_spec=None) -> str:
        messages = [dict(role='system', content=content)]
        for hist in self.history:
            messages.append(dict(role=hist['role'], content=hist['content']))
        messages.append(dict(role='user', content=input_text))
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                functions=functions_spec,
                function_call='auto',
                **self.model_params
            ).get('choices')[0].get('message', {})
        except KeyError:
            response = {"error": "Key Error [0]. Do not have enough information."}
        result = {'result': None, 'message': response.get('content', "")}
        function_call = response.get('function_call')
        if function_call:
            function_name = function_call['name']
            function_kwds = json.loads(function_call['arguments'].replace('\n', ''))
            try:
                function_response = functions[function_name](**function_kwds)
            except TypeError as ex:
                function_response = str(ex)
            call_result = {'name': function_name, 'arguments': str(function_kwds)}
            result = {'result': function_response, 'function_call': str(call_result)}
            self.save_history(messages[-1], dict(role='assistant', content=function_response, function_call=str(call_result)))
        else:
            self.save_history(messages[-1], dict(role='assistant', content=response.get('content', "")))
        return result
