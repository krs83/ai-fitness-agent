from pydantic import BaseModel, Field

# Пока сохраняем на лету БЕЗ БД
exercises_db = {}


# Модель для упражнения
class Exercise(BaseModel):
    """Эта функция позволяет добавлять информацию о сделанном в зале упражнении."""

    exercise_type: str = Field(
        default=None, description="Тип упражнения (кардио или силовое)"
    )
    name: str = Field(default=None, description="Название упражнения")
    sets: int = Field(default=None, description="Количество подходов")
    reps: int = Field(default=None, description="Количество повторений")
    breaks: int = Field(default=1, description="Перерыв между подходами в минутах")

    def process(self, session_id):
        """Обрабатывает добавление упражнения"""
        if session_id not in exercises_db:
            exercises_db[session_id] = []
        exercises_db[session_id].append(self)
        return "Упражнение добавлено"


class ListExercises(BaseModel):
    """Эта функция позволяет получить список сделанных упражнений"""

    def process(self, session_id):
        """Возвращает список упражнений для сессии"""
        if session_id not in exercises_db:
            return "Упражнений нет"
        else:
            return "\n".join(
                [
                    f"{i+1}. {x.name} ({x.exercise_type}, {x.sets} подходов), {x.reps} повторений"
                    for i, x in enumerate(exercises_db[session_id])
                ]
            )
