import json
from datetime import datetime
from langchain.schema.messages import HumanMessage , AIMessage
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
print(config)

def save_chat_history_json(chat_history,file_path):
    with open(file_path, "w") as f:
        json_data = [message.dict() for message in chat_history]
        json.dump(json_data,f)

def load_chat_history_json(file_path):
    with open(file_path,"r") as f:
        json_data = json.load(f)
        messages = [HumanMessage(**message)if message["type"] == "human" else AIMessage(**message) for message in json_data]
        return messages


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_avatar(sender_type):
    if sender_type == "human":
        return "chat_icons/user_image.png"
    else:
       return "chat_icons/bot_image.png"