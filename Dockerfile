FROM python:3.13-slim

WORKDIR /gs_agent

# Создаём папку для кэша модели
RUN mkdir -p /root/.cache/fastembed && chmod -R 777 /root/.cache

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Предварительно скачиваем модель
RUN python -c "from fastembed import TextEmbedding; TextEmbedding('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"

# Копируем весь проект
COPY . .

# Создаём папки для базы и логов с правильными правами
RUN mkdir -p /gs_agent/gs_db /gs_agent/logs && \
    chown -R 1000:1000 /gs_agent && \
    chmod -R 755 /gs_agent

# Переключаемся на не-root пользователя
USER 1000

# Точка входа
CMD ["python", "-m", "main"]

