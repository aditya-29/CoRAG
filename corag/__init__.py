from .prompts import prompts as Prompts
from .prompts.task_description import Task
from .chat.base_chat import BaseChat

import os
import yaml

# export the keys
def load_secrets(file_path = "../secrets.txt"):
    if not os.path.exists(file_path):
        print("[WARN] No secrets file found")
    
    with open(file_path, "r") as file:
        secrets = yaml.safe_load(file)  # Safe load prevents arbitrary code execution

    for key, value in secrets.get("api_keys", {}).items():
        env_var_name = key.upper()
        os.environ[env_var_name] = value

        print(f"Exported {env_var_name} to environment variable")


load_secrets()
    
    
    
    
    
    