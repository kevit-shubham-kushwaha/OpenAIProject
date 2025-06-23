from dotenv import dotenv_values
import os

env_path = ".env"

if os.path.exists(env_path) is None:
    os.makedirs(os.path.dirname(env_path), exist_ok=True)

config = dotenv_values(env_path)


HOST = config.get("HOST")
PORT = config.get("PORT")

OPENAI_API_KEY  = config.get("OPENAI_API_KEY")
OPENAI_MODEL_NAME = config.get("OPENAI_MODEL_NAME","gpt-4o")
OPENAI_ASSISTANT_ID = config.get("OPENAI_ASSISTANT_ID")
OPENWEATHER_API_KEY = config.get("OPENWEATHER_API_KEY")
