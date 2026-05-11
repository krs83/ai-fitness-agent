import io
import sys

from dotenv import load_dotenv

from agent import Agent
from func_tools import Exercise, ListExercises, SearchDocs

if sys.platform == 'linux':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

load_dotenv()


instructions = """
Ты — опытный фитнес-тренер, задача которого — помочь мне тренироваться в зале. Ты можешь
советовать упражнения, давать рекомендации по питанию и т. д. Ты также можешь вести 
дневник выполненных пользователем упражнений - для этого используй функцию `Exercise`. Чтобы
показать список выполненных упражнений, используй `ListExercises`.

ВАЖНО: Для ответа на ЛЮБЫЕ вопросы о клубе, тренерах, расписании, правилах — ОБЯЗАТЕЛЬНО 
используй инструмент SearchDocs.
НЕ отвечай на такие вопросы из своих знаний, даже если кажется, что знаешь.
"""


fit_agent = Agent(instructions, tools=[Exercise, ListExercises, SearchDocs])

# Общение с агентом
SESSION_ID = "my_session"

while True:
    user_input = input("Вы: ")
    if user_input.lower() == "выход":
        break
    response = fit_agent(user_input, session_id=SESSION_ID)
    print(f"Тренер: {response.output_text}")

