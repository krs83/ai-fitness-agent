from dotenv import load_dotenv

from agent import Agent
from func_tools import Exercise, ListExercises, SearchDocs

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
response = fit_agent("Как зовут тренера и какие у него достижения?")
print(response.output_text)

response = fit_agent("Напомни, какие я сделал упражнения?")
print(response.output_text)

