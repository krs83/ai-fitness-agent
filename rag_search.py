import chromadb
from fastembed import TextEmbedding
import os

from log_config import get_logger

logger = get_logger(__name__)
EMB_MODEL = os.getenv("EMBEDDING_MODEL")

# 1. Загружаем лёгкую модель эмбеддингов
embedding_model = TextEmbedding(model_name=EMB_MODEL)

# 2. Подключаем ChromaDB (сохраняется на диск)
client = chromadb.PersistentClient(path="./gs_db")

# 3. Создаём коллекцию (без встроенной функции эмбеддингов)
collection = client.get_or_create_collection(name="gs_knowledge")

# 4. Загружаем .md файл
if collection.count() == 0:
    docs_dir = "docs"
    for filename in os.listdir(docs_dir):
        if filename.endswith(".md"):
            with open(os.path.join(docs_dir, filename), "r", encoding="utf-8") as f:
                content = f.read()

            # Генерируем эмбеддинг для документа
            embedding = list(embedding_model.embed([content]))[0]

            # Добавляем в Chroma с готовым вектором
            collection.add(
                documents=[content],
                embeddings=[embedding],
                ids=[filename.replace(".md", "")],
                metadatas=[{"source": filename}]
            )
            logger.info(f"Файл {filename} добавлен!")

# 5. Функция поиска
def search_knowledge(query: str, n_results: int = 3) -> str:
    # Генерируем эмбеддинг для запроса
    query_embedding = list(embedding_model.embed([query]))[0]

    # Ищем в Chroma
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    if not results["documents"][0]:
        logger.info("Информация не найдена")

    return "\n\n".join(results["documents"][0])

