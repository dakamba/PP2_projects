import json

def save_settings(data):
    """
    Сохраняет текущие настройки игры (тип машины, карту, сложность) в файл settings.json.
    Используется отступ indent=4 для того, чтобы файл был читаемым для человека.
    """
    with open('settings.json', 'w') as f:
        json.dump(data, f, indent=4)

def load_leaderboard():
    """
    Загружает список рекордов из файла leaderboard.json.
    Если файла еще не существует (первый запуск), возвращает пустой список.
    """
    try:
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Если файла нет, возвращаем пустой список, чтобы не было ошибки в коде
        return []
    except Exception:
        return []
        
def load_settings():
    """
    Загружает настройки игры. Если файла нет, создает словарь с параметрами по умолчанию.
    """
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except:
        # Важные значения по умолчанию: средняя сложность и 1000м дистанции
        return {
            "road_type": "Summer", 
            "car_type": "Player_blue", 
            "difficulty": 1, 
            "sound": True, 
            "finish_distance": 1000
        }

def save_score(name, score, distance, coins):
    """
    Добавляет новый результат в таблицу лидеров, сортирует её и сохраняет ТОП-10.
    """
    # 1. Сначала загружаем текущие рекорды
    data = load_leaderboard()
    
    # 2. Добавляем новый результат (словарь с именем, очками, дистанцией и монетами)
    data.append({
        "name": name, 
        "score": score, 
        "distance": distance, 
        "coins": coins
    })
    
    # 3. Сортировка:
    # key=lambda x: x['score'] — сортируем по ключу 'score'
    # reverse=True — от большего к меньшему
    # [:10] — берем только первые 10 элементов (срез)
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    
    # 4. Записываем обновленный ТОП-10 обратно в файл
    with open('leaderboard.json', 'w') as f:
        json.dump(data, f, indent=4)