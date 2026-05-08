from dotenv import load_dotenv

from agent import Agent
from func_tools import Exercise, ListExercises

load_dotenv()


instructions = """
Ты — опытный фитнес-тренер, задача которого — помочь мне тренироваться в зале. Ты можешь
советовать упражнения, давать рекомендации по питанию и т. д. Ты также можешь вести 
дневник выполненных пользователем упражнений - для этого используй функцию `Exercise`. Чтобы
показать список выполненных упражнений, используй `ListExercises`.
"""


fit_agent = Agent(instructions, tools=[Exercise, ListExercises])

# Общение с агентом
response = fit_agent("Я прошел 10000 шагов и сделал 4 подхода отжиманий по 20 раз, запиши!")
print(response.output_text)

response = fit_agent("Напомни, какие я сделал упражнения?")
print(response.output_text)

