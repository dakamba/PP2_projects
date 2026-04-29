import json
import os

# Определяем корень папки, где лежит этот скрипт
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Пути к файлам теперь всегда привязаны к папке проекта
SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')
LEADERBOARD_PATH = os.path.join(BASE_DIR, 'leaderboard.json')

def save_settings(data):
    """Сохранение настроек в JSON"""
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def load_leaderboard():
    """Загрузка списка рекордов (Топ-10)"""
    try:
        with open(LEADERBOARD_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
        
def load_settings():
    """Загрузка настроек или возврат дефолтных"""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    except:
        return {
            "road_type": "Summer", 
            "car_type": "Player_blue", 
            "difficulty": 1, 
            "sound": True, 
            "finish_distance": 1000
        }

def save_score(name, score, distance, coins):
    """Добавление нового рекорда и перезапись файла"""
    data = load_leaderboard()
    
    data.append({
        "name": name, 
        "score": score, 
        "distance": distance, 
        "coins": coins
    })
    
    # Сортировка по убыванию очков и срез топ-10
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    
    with open(LEADERBOARD_PATH, 'w') as f:
        json.dump(data, f, indent=4)