tools = [
    {
        "type": "function",
        "name": "log_exercise",
        "description": "Записывает информацию о выполненном упражнении в журнал тренировок",
        "parameters": {
            "type": "object",
            "properties": {
                "exercise_name": {
                    "type": "string",
                    "description": "Название упражнения",
                },
                "sets": {"type": "integer", "description": "Количество подходов"},
                "reps": {
                    "type": "integer",
                    "description": "Количество повторений в каждом подходе",
                },
                "weight": {
                    "type": "number",
                    "description": "Вес в кг (если применимо)",
                },
                "date": {
                    "type": "string",
                    "description": "Дата тренировки в формате YYYY-MM-DD",
                },
            },
            "required": ["exercise_name", "sets", "reps"],
        },
    },
    {
        "type": "function",
        "name": "get_exercise_history",
        "description": "Получает историю тренировок пользователя за указанное количество дней",
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "За сколько последних дней получить историю (по умолчанию 7)",
                }
            },
            "required": [],
        },
    },
    {
        "type": "function",
        "name": "calculate_calories",
        "description": "Рассчитывает примерное количество сожжённых калорий во время тренировки",
        "parameters": {
            "type": "object",
            "properties": {
                "exercise_name": {
                    "type": "string",
                    "description": "Название упражнения",
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Продолжительность упражнения в минутах",
                },
                "intensity": {
                    "type": "string",
                    "enum": ["low", "moderate", "high"],
                    "description": "Интенсивность тренировки: low (низкая), moderate (средняя), high (высокая)",
                },
                "weight": {
                    "type": "number",
                    "description": "Вес пользователя в килограммах",
                },
            },
            "required": ["exercise_name", "duration_minutes"],
        },
    },
]
