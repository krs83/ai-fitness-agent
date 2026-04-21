from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

class Assistant:
    def __init__(self, instructions):
        self.folder_id = os.getenv("FOLDER_ID")
        self.api_key = os.getenv("API_KEY")
        self.instructions = instructions
        self.previous_response_id_map = {}
        self.history = []
        self.model = f"gpt://{self.folder_id}/qwen3-235b-a22b-fp8/latest"
        self.client = OpenAI(
            base_url = "https://ai.api.cloud.yandex.net/v1",
            api_key = self.api_key,
            project = self.folder_id
        )

    def __call__(self, input, session_id="default"):
        # Получитить ID предыдущего сообщения для данной сессии
        previous_response_id = self.previous_response_id_map.get(session_id, None)

        # Сформировать ответ модели
        res = self.client.responses.create(
            model = self.model,
            store = True,
            # previous_response_id = previous_response_id,
            instructions = self.instructions,
            max_output_tokens = 100,
            input = input
        )

        # Записать ID последнего ответа модели в словаре
        self.previous_response_id_map[session_id] = res.id
        self.history.append(f"Вопрос: {input}\n Ответ: {res.output_text}")
        print(f"ИСТОРИЯ ПЕРЕПИСКИ:\n {self.history}")
        return res.output_text

wrong_promt = "Извините, но я не обсуждаю другие темы кроме спорта"
instructions = ("Ты — опытный фитнес-тренер, задача которого — помочь мне тренироваться в зале c гирями."
                f"Не обсуждай другие темы кроме  спорта. На другие темы отвечай {wrong_promt}")

fitness_agent = Assistant(instructions)
print(fitness_agent(input="Привет, хочу тренироваться с гирями 16 и 24 кг"))
print(fitness_agent(input="мой уровень средний. 16 кг для меня не очень тяжелая гиря"))


