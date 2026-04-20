from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

folder_id = os.getenv("FOLDER_ID")
api_key = os.getenv("API_KEY")

client = OpenAI(
    base_url = "https://ai.api.cloud.yandex.net/v1",
    api_key = api_key,
    project = folder_id
)

model = f"gpt://{folder_id}/qwen3-235b-a22b-fp8/latest"

res = client.responses.create(
    model = model,
    instructions = "Ты — опытный фитнес-тренер, задача которого — помочь мне тренироваться в зале.",
    input = "Привет! С чего ты порекомендуешь начать тренировки в зале?"
)

print(res.output_text)

