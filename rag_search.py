import chromadb
from fastembed import TextEmbedding
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:    %(asctime)s - %(name)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

logger = logging.getLogger(__name__)

# 1. Загружаем лёгкую модель эмбеддингов
embedding_model = TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# 2. Подключаем ChromaDB (сохраняется на диск)
client = chromadb.PersistentClient(path="./fitness_db")

# 3. Создаём коллекцию (без встроенной функции эмбеддингов)
collection = client.get_or_create_collection(name="fitness_knowledge")

# 4. Загружаем .md файл
if collection.count() == 0:
    docs_dir = "docs"
    for filename in os.listdir(docs_dir):
        if filename.endswith(".md"):
            with open(os.path.join(docs_dir, filename), "r", encoding="utf-8") as f:
                content = f.read()

            # Генерируем эмбеддинг для документа
            emmbedding = list(embedding_model.embed([content]))[0]

            # Добавляем в Chroma с готовым вектором
            collection.add(
                documents=[content],
                embeddings=[emmbedding],
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
        logger.info("Иформация не найдена")

    return "/n/n".join(results["documents"][0])

