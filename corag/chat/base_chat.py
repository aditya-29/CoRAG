class BaseChat:
    def __init__(self, model_name):
        print(f"[INFO] using the model : {model_name}")

    def chat(self, chat_inputs: dict):
        raise Exception("chat function is not implemented")
    
