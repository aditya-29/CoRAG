from openai import OpenAI
import requests
import os

from . import BaseChat

class GPT(BaseChat):
    def __init__(self, 
                 model_name = "o3-mini-2025-01-31",
                 temperature = 0.7,
                 max_tokens = 100):
        super().__init__(model_name)
        self._model_name = model_name
        self._temperature = temperature
        self._max_tokens = max_tokens

        self.url = "https://api.openai.com/v1/chat/completions"
        self.api_key = self.__load_api_key()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }


    def __load_api_key(self):
        key = os.getenv("OPENAI_API_KEY", "NOT-FOUND")

        if key == "NOT-FOUND":
            raise Exception("OPENAI API KEY not found in env variables")
        
        return key
    
    def format_input(self, system: str, user: list, assistant: list):
        output = []

        if system is not None:
            temp = {"role" : "system", "content" : system}
            output.append(temp)

        for i in range(len(user)):
            if i < len(user):
                temp = {"role" : "user", "content" : user[i]}
                output.append(temp)
            
            if i < len(assistant):
                temp = {"role" : "user", "content" : assistant[i]}
                output.append(temp)
        
        return output

    def chat(self, chat_inputs: dict, raw_output = False, logprobs = None):
        # retrieve the inputs
        user_messages = chat_inputs.get("user", [])
        system_message = chat_inputs.get("system", None)
        assistant_messages = chat_inputs.get("assistant", [])

        formatted_input = self.format_input(system = system_message,
                                            user = user_messages,
                                            assistant = assistant_messages)


        data = {
            "model": self._model_name,  
            "messages": formatted_input,
            "temperature": self._temperature, 
            "max_tokens": self._max_tokens,
            "logprobs" : logprobs
        }

        response = requests.post(self.url, headers = self.headers, json = data)

        if response.status_code == 200:
            raw_result = response.json()
            output = raw_result["choices"][0]["message"]["content"]

        if raw_output:
            return raw_result
        return output


