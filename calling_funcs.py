import uuid
from datetime import datetime, timedelta

exercises_db = {
    "users": {},
    "exercise_log": []
}

# Функции для работы с данными
def log_exercise(exercise_name,
                 sets,
                 reps,
                 weight=None,
                 date=None):
    """
Записывает информацию о выполненном упражнении в журнал тренировок

Args:
    exercise_name (str): Название упражнения
    sets (int): Количество подходов
    reps (int): Количество повторений в каждом подходе
    weight (float, optional): Вес в кг
    date (str, optional): Дата тренировки в формате YYYY-MM-DD

Returns:
    dict: Информация о записи с уникальным ID
"""

    # Генерируем уникальный ID для записи
    record_id = str(uuid.uuid4())

    # Устанавливаем текущую дату, если не указана
    if date is None:
        date = datetime.now().strftime("%y-%m-%d")

    # Создаём запись
    record = {
        "id": record_id,
        "exercise": exercise_name,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "date": date
    }

    # Пока сохраняем на лету БЕЗ БД
    if "exercise_log" not in exercises_db:
        exercises_db["exercise_log"] = []

    exercises_db["exercise_log"].append(record)

    return {
        "status": "success",
        "message": f"Упражение '{exercise_name}' успешно записано",
        "record_id": record_id
    }

def get_exercise_history(user_id="default", days=7):
    """
    Получает историю тренировок пользователя за указанное количество дней

    Args:
        user_id (str): Идентификатор пользователя
        days (int): Количество дней для истории

    Returns:
        list: Записи о тренировках
    """
    # Определите дату начала периода
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%M-%D")

    # Отфильтруйте записи по пользователю и дате
    history = [
        record for record in exercises_db["exercise_log"]
        if record.get("user_id") == user_id and record.get("date") >= start_date
    ]

    return {
        "status": "success",
        "history": history
    }

def calculate_calories(exercise_name,
                       duration_minutes,
                       intensity="moderate",
                       weight_kg=44):
    """
    Рассчитывает примерное количество сожжённых калорий

    Args:
        exercise_name (str): Название упражнения
        duration_minutes (int): Продолжительность в минутах
        intensity (str): Интенсивность (low, moderate, high)
        weight_kg (float): Вес пользователя в кг

    Returns:
        dict: Информация о сожжённых калориях
    """
    # Приблизительные значения MET (метаболический эквивалент задачи)
    # для различных упражнений и интенсивностей
    met_values = {
        "бег": {"low": 7, "moderate": 9, "high": 12},
        "ходьба": {"low": 3, "moderate": 4, "high": 5},
        "плавание": {"low": 5, "moderate": 7, "high": 10},
        "велосипед": {"low": 4, "moderate": 6, "high": 8},
        "приседания": {"low": 3, "moderate": 5, "high": 7},
        "отжимания": {"low": 3, "moderate": 5, "high": 8},
        # Для неизвестных упражнений
        "default": {"low": 3, "moderate": 5, "high": 7},
    }

    # Вы получите MET для указанного упражнения и интенсивности
    exercise_name_lower = exercise_name.lower()
    exercise_met = met_values.get(exercise_name_lower, met_values["default"])
    met = exercise_met.get(intensity, exercise_met["moderate"])

    # Формула для расчёта калорий: MET × вес (кг) × время (часы)
    calories = met * weight_kg * (duration_minutes / 60)

    return {
        "status": "success",
        "exercise": exercise_name,
        "duration_minutes": duration_minutes,
        "intensity": intensity,
        "calories_burned": round(calories, 1),
        "met_used": met
    }