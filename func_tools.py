from pydantic import BaseModel, Field

from rag_search import search_knowledge


class SearchDocs(BaseModel):
    """Ищет информацию в документации зала для занятий джиу-джитсу"""

    query: str = Field(description="Поисковый запрос пользователя")

    def process(self, session_id):
        return search_knowledge(self.query, n_results=2)