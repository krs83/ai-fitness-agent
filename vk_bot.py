import os
import sys

import vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dotenv import load_dotenv
from vk_api.utils import get_random_id

from agent import Agent
from log_config import get_logger

load_dotenv()
logger = get_logger(__name__)

VK_KEY = os.getenv("VK_API_KEY")
GROUP_ID = os.getenv("VK_GROUP_ID")

def init_vk_bot(agent: Agent):
    """Инициализирует и запускает ВК-бота"""
    if not VK_KEY or not GROUP_ID:
        logger.warning("VK_TOKEN или GROUP_ID не заданы в .env")
        sys.exit(1)

    # Подключаемся к ВК
    vk_session = vk_api.VkApi(token=VK_KEY)
    vk_session.http.timeout = 60
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)

    logger.info("✅ ВК-бот запущен!")

    # Основной цикл обработки сообщений
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            try:
                # Получаем сообщение
                message = event.object.message
                user_text = message.get("text", "")
                user_id = message.get("from_id")
                peer_id = message.get("peer_id")

                # Игнорируем пустые сообщения
                if not user_text.strip():
                    continue

                logger.info(f"📩 Новое сообщение от {user_id}: {user_text[:50]}...")

                # Отправляем статус "печатает"
                vk.messages.setActivity(peer_id=peer_id, type="typing")

                # Вызываем агента
                response = agent(user_text, session_id=str(user_id))
                logger.info(f"Вызываем агента с {user_id=}")

                # Отправляем ответ
                if response and response.output_text:
                    answer = response.output_text
                    random_id=get_random_id()
                    logger.info(f"Отправляем ответ: {answer}")

                    vk.messages.send(peer_id=peer_id, message=answer, random_id=random_id)
                    logger.info(f"✅ Ответ отправлен пользователю: \n{user_id=}\n{peer_id=}\n{random_id=}\n ")
            except Exception as e:
                logger.error(f"❌ Ошибка обработки сообщения: {e}")
