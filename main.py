import json

from dotenv import load_dotenv
from openai import OpenAI
import os

from ai_tools import tools
from calling_funcs import log_exercise, get_exercise_history, calculate_calories

load_dotenv()


class Assistant:
    def __init__(self, instructions: str, tools=None, function_map=None):
        self.folder_id = os.getenv("FOLDER_ID")
        self.api_key = os.getenv("API_KEY")
        self.instructions = instructions
        self.previous_response_id_map = {}
        self.tools = tools or {}
        self.function_map = {
            "log_exercise": log_exercise,
            "get_exercise_history": get_exercise_history,
            "calculate_calories": calculate_calories
        }
        self.exercises_db = {}
        self.history = []
        self.model = f"gpt://{self.folder_id}/deepseek-v32/latest"
        self.client = OpenAI(
            base_url="https://ai.api.cloud.yandex.net/v1",
            api_key=self.api_key,
            project=self.folder_id,
        )

    def __call__(self, input_text, session_id="default"):
        # Получить ID предыдущего сообщения для данной сессии
        previous_response_id = self.previous_response_id_map.get(session_id, None)

        # Сформировать ответ модели
        response = self.client.responses.create(
            model=self.model,
            store=True,
            previous_response_id=previous_response_id,
            instructions=self.instructions,
            # max_output_tokens=100,
            input=input_text,
            tools=self.tools,
        )

        # Обновление ID ответа
        self.previous_response_id_map[session_id] = response.id

        # Обработка ответа (включая возможные вызовы функций)
        return self._process_response(response, session_id)

    def _process_response(self, response, session_id):
        """Обрабатывает ответ модели, включая возможные вызовы функций"""

        # Проверка наличия вызова функций
        for output_item in response.output:
            if output_item.type == "function_call":
                # Извлечение данных вызова
                function_name = output_item.name
                arguments_str = output_item.arguments

                # Парсинг аргументов из JSON-строки
                function_args = json.loads(arguments_str)

                print(f"[DEBUG] Вызов функции: {function_name}({function_args})")

                # Вызов функции, если она есть в маппинге
                if function_name in self.function_map:
                    function_result = self.function_map[function_name](**function_args)

                    print(f"[DEBUG] Результат функции: {function_result}")

                    # Формирование сообщения с результатом
                    result_message = f"Результат выполнения функции {function_name}: {json.dumps(function_result, ensure_ascii=False)}"

                    # Отправление результата обратно модели
                    follow_up = self.client.responses.create(
                        model=self.model,
                        store=True,
                        previous_response_id=response.id,
                        input=result_message
                    )

                    # Обновление ID последнего ответа
                    self.previous_response_id_map[session_id] = follow_up.id

                    # Рекурсивная обработка нового ответа
                    # (модель может вызвать ещё одну функцию)
                    return self._process_response(follow_up, session_id)

        # Если вызовов функций нет, возвращается текстовый ответ
        return response.output_text if hasattr(response, "output_text") else ""

instructions = """
Ты — профессиональный фитнес-ассистент спортивного клуба SuperGYM. 
Твоя задача — помогать пользователям:
1. Отвечать на вопросы о фитнесе, тренировках и здоровом образе жизни
2. Записывать информацию о выполненных упражнениях
3. Предоставлять историю тренировок
4. Рассчитывать сожжённые калории


Общайся энергично и мотивирующе. Предлагай конкретные рекомендации, 
основанные на данных пользователя.
"""


fitness_assistant = Assistant(instructions, tools=tools)


print(fitness_assistant("Привет! Я сегодня сделал 4 подхода по 10 отжиманий. Мой user_id 1. Запиши это."))
# Ассистент использует log_exercise и возвращает ответ


print(fitness_assistant("Сколько калорий я сжёг за 30 минут бега с высокой интенсивностью? Мой user_id 1"))
# Ассистент использует calculate_calories и возвращает ответ


print(fitness_assistant("Покажи историю моих тренировок. Мой user_id 1"))
# Ассистент использует get_exercise_history и возвращает ответ

print(fitness_assistant("Привет! Я сегодня сделал 5 подхода по 12 отжиманий.Мой user_id 1 Запиши это."))
# Ассистент использует log_exercise и возвращает ответ


print(fitness_assistant("Сколько калорий я сжёг за отжимания с высокой интенсивностью? Мой user_id 1"))
# Ассистент использует calculate_calories и возвращает ответ


print(fitness_assistant("Покажи историю моих тренировок. Мой user_id 1"))
# Ассистент использует get_exercise_history и возвращает ответ
