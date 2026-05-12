import json
import os

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

from log_config import get_logger

load_dotenv()
logger = get_logger(__name__)


class Agent:
    def __init__(self, instruction: str, tools=None, model=os.getenv("MODEL")):
        self.instructions = instruction
        self.tools = [self._create_tool_annot(x) for x in tools]
        self.tool_map = {
            x.__name__: x
            for x in tools
            if not isinstance(x, dict) and issubclass(x, BaseModel)
        }
        self.user_sessions = {}
        self.model = model
        self.client = OpenAI(
            base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY")
        )

    def __call__(self, message, session_id="default"):
        """Обрабатывает сообщение пользователя"""
        s = self.user_sessions.get(
            session_id,
            {
                "previous_response_id": None,
                "history": [],
            },
        )
        s["history"].append({"role": "user", "content": message})

        # Вызов модели с инструментами
        response = self.client.responses.create(
            model=self.model,
            store=True,
            tool_choice="auto",
            tools=self.tools,
            instructions=self.instructions,
            previous_response_id=s["previous_response_id"],
            input=message,
        )

        # Обработка вызова инструментов
        tool_calls = [item for item in response.output if item.type == "function_call"]
        if tool_calls:
            s["history"].append({"role": "func_call", "content": response.output_text})
            out = []
            for call in tool_calls:
                logger.info(f"Обработка: {call.name} ({call.arguments})")
                try:
                    fn = self.tool_map[call.name]
                    args = call.arguments or {}
                    obj = fn.model_validate(json.loads(args))
                    result = obj.process(session_id)
                except Exception as e:
                    result = f"Ошибка: {e}"
                out.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": result,
                    }
                )
            # Отправка результатов обратно модели
            response = self.client.responses.create(
                model=self.model,
                store=True,
                tools=self.tools,
                previous_response_id=response.id,
                input=out,
            )
            # Сохранение состояния
            if response.status == "incomplete":
                logger.error(
                    f"WARNING: Incomplete response status. Reason:{response.incomplete_details.reason}"
                )
            else:
                s["previous_response_id"] = response.id
            s["history"].append(
                {"role": "assistant", "content": response.output_text}
            )
            self.user_sessions[session_id] = s
        return response

    @staticmethod
    def _create_tool_annot(x):
        """Создаёт описание инструмента для API"""
        if isinstance(x, dict):
            return x
        if issubclass(x, BaseModel):
            return {
                "type": "function",
                "name": x.__name__,
                "description": x.__doc__,
                "parameters": x.model_json_schema(),
            }
        else:
            return x
