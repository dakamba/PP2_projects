import pygame
import sys
import random
# Импортируем кастомные классы и функции из твоих файлов проекта
from ui import Button, load_car_sprites
from racer import *
from persistence import load_settings, save_settings, save_score, load_leaderboard
import os

# Получаем абсолютный путь к папке, где лежит main.py
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# --- ИНИЦИАЛИЗАЦИЯ ДВИЖКА ---
pygame.init() # Запуск всех модулей Pygame

# Настройка размеров окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Установка заголовка окна (полезно для идентификации проекта)
pygame.display.set_caption("Racer Game - TSIS 3")

# Объект для контроля частоты кадров (FPS)
clock = pygame.time.Clock()

# Списки доступных названий ассетов (машин и фонов дорог)
CARS = ["Player_blue", "Player_green", "Player_red", "Player_yellow", "Police"]
ROADS = ["Summer", "Winter", "Desert", "Highway"]

# Загружаем настройки пользователя из JSON файла при старте
settings = load_settings()

# Глобальная переменная для хранения имени игрока (по умолчанию Гость)
current_user = "Guest"

def update_game_assets():
    """
    Функция для динамической загрузки графики (дороги и машины) 
    на основе текущих настроек пользователя.
    """
    # Извлекаем тип дороги и машины из словаря settings (по умолчанию Summer и Blue)
    r_type = settings.get("road_type", "Summer")
    c_type = settings.get("car_type", "Player_blue")
    
    try:
        #Получаем название файла для дорог
        size_str = "(96 x 64)" if r_type == "Highway" else "(64 x 64)"
        road_path = os.path.join(BASE_PATH, "assets", "Levels", f"{r_type}_road {size_str}.png")
        
        # Загружаем изображение дороги и оптимизируем для работы с прозрачностью
        road = pygame.image.load(road_path).convert_alpha()
        # Растягиваем картинку под размер игрового окна
        road = pygame.transform.scale(road, (WIDTH, HEIGHT))
        
        # Формируем путь к спрайту машины и загружаем его через вспомогательную функцию
        car_path = os.path.join(BASE_PATH, "assets", "Cars", f"{c_type}.png")
        car = load_car_sprites(car_path, 5) # 5 — количество кадров в анимации/спрайте
        
    except Exception as e:
        # Если файлы не найдены или произошла ошибка, создаем временные заглушки
        print(f"Ошибка загрузки: {e}")
        road = pygame.Surface((WIDTH, HEIGHT)) # Просто пустой холст
        road.fill((50, 50, 50))               # Серого цвета (асфальт)
        # Создаем список пустых поверхностей для машины, чтобы код не "падал"
        car = [pygame.Surface((80, 80)) for _ in range(8)]
        
    return road, car

# Первичная загрузка ассетов перед запуском меню
road_img, car_sprites = update_game_assets()

# --- ЭКРАНЫ ИНТЕРФЕЙСА ---

def username_screen():
    """
    Экран для ввода имени игрока. 
    Позволяет печатать текст и сохраняет его в глобальную переменную.
    """
    global current_user
    name = "" # Локальная переменная для хранения вводимых символов
    font = pygame.font.SysFont("Impact", 45) # Шрифт в стиле "гоночных" игр
    
    while True:
        screen.fill((20, 20, 20)) # Заливка фона темно-серым цветом
        
        # Рендерим (рисуем) статичный текст инструкции
        txt = font.render("ENTER YOUR NAME:", True, (255, 255, 255))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 200))
        
        # Рендерим текущее вводимое имя с символом курсора "|"
        name_surf = font.render(name + "|", True, (0, 255, 0)) # Зеленый текст
        screen.blit(name_surf, (WIDTH//2 - name_surf.get_width()//2, 300))

        # Обработка ввода с клавиатуры
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
                
            if event.type == pygame.KEYDOWN:
                # Если нажат Enter и имя не пустое — сохраняем и выходим из экрана
                if event.key == pygame.K_RETURN and name:
                    current_user = name
                    return
                # Удаление последнего символа (Backspace)
                elif event.key == pygame.K_BACKSPACE: 
                    name = name[:-1]
                # Добавление нового символа (если длина имени меньше 12)
                elif len(name) < 12: 
                    # event.unicode содержит символ, который нажал пользователь
                    name += event.unicode
                    
        pygame.display.flip() # Обновляем экран
        clock.tick(60)        # Ограничиваем цикл до 60 FPS


def leaderboard_screen():
    """
    ЭКРАН ТАБЛИЦЫ РЕКОРДОВ
    Отображает топ-10 игроков, загруженных из файла leaderboard.json.
    """
    # Создаем кнопку возврата в главное меню
    btn_back = Button("BACK", WIDTH//2 - 100, 520, 200, 50, (100, 100, 100), (150, 150, 150))
    
    # Загружаем список словарей с рекордами через функцию из persistence.py
    scores = load_leaderboard()
    
    # Настройка шрифтов: Impact для заголовка, Arial для данных
    font_t = pygame.font.SysFont("Impact", 50)
    font_r = pygame.font.SysFont("Arial", 22, bold=True)

    while True:
        # Темно-синий/серый фон для экрана рекордов
        screen.fill((25, 25, 30))
        
        # Отрисовка заголовка "TOP 10 RACERS" по центру
        title = font_t.render("TOP 10 RACERS", True, (255, 215, 0)) # Золотистый цвет
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        # Отрисовка шапки таблицы (выравнивание с помощью f-строк)
        # :<15 означает выделение 15 символов с выравниванием по левому краю
        header_str = f"{'NAME':<15} {'SCORE':<10} {'DIST':<10} {'COINS':<5}"
        header = font_r.render(header_str, True, (200, 200, 200))
        screen.blit(header, (WIDTH//2 - 250, 130))

        # Перебор первых 10 записей из списка рекордов
        for i, entry in enumerate(scores[:10]):
            # Формируем строку данных для каждого игрока
            # Делим дистанцию на 10 для отображения в метрах
            name = entry.get('name', '???')
            pts = entry.get('score', 0)
            dist = entry.get('distance', 0) // 10
            cns = entry.get('coins', 0)
            
            txt_row = f"{name:<15} {pts:<10} {dist:<10} {cns:<5}"
            row_surf = font_r.render(txt_row, True, (255, 255, 255))
            
            # Смещение каждой строки на 30 пикселей вниз (i * 30)
            screen.blit(row_surf, (WIDTH//2 - 250, 170 + i * 30))

        # Отрисовка кнопки
        btn_back.draw(screen)
        
        # Обработка событий выхода и клика по кнопке
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
                
            if btn_back.is_clicked(event): 
                return # Возврат в функцию main_menu()
                
        pygame.display.flip()
        clock.tick(60)


def settings_screen():
    """
    ЭКРАН НАСТРОЕК: ПОЗВОЛЯЕТ ИЗМЕНЯТЬ ПАРАМЕТРЫ МАШИНЫ, КАРТЫ, ЦЕЛИ И СЛОЖНОСТИ.
    """
    # Используем глобальные переменные, чтобы изменения применились ко всей игре сразу
    global settings, road_img, car_sprites
    
    # Список для текстового отображения уровней сложности
    DIFFICULTIES = ["Easy", "Medium", "Hard"]
    
    # Получаем текущие индексы из настроек, чтобы знать, на чем остановился пользователь
    # .index() находит позицию текущего элемента в списках CARS и ROADS
    car_idx = CARS.index(settings.get("car_type", "Player_blue"))
    road_idx = ROADS.index(settings.get("road_type", "Summer"))
    dist_val = settings.get("finish_distance", 1000)
    diff_idx = settings.get("difficulty", 1) 

    # Инициализация кнопок переключения (координата X=550 выравнивает их в один ряд справа)
    btn_next_car = Button(">", 550, 150, 50, 40, (100, 100, 100), (150, 150, 150))
    btn_next_road = Button(">", 550, 220, 50, 40, (100, 100, 100), (150, 150, 150))
    btn_next_dist = Button(">", 550, 290, 50, 40, (100, 100, 100), (150, 150, 150))
    btn_next_diff = Button(">", 550, 360, 50, 40, (100, 100, 100), (150, 150, 150))
    
    # Кнопка сохранения (находится внизу по центру WIDTH//2 - 100)
    btn_save = Button("SAVE & BACK", WIDTH//2 - 100, 480, 200, 50, (46, 204, 113), (39, 174, 96))

    font = pygame.font.SysFont("Impact", 30)

    while True:
        screen.fill((30, 30, 30)) # Темно-серый фон окна настроек
        
        # Отрисовка текущих выбранных значений на экране
        # Каждое значение выводится слева от соответствующей кнопки
        screen.blit(font.render(f"CAR: {CARS[car_idx]}", True, (255, 255, 255)), (200, 155))
        screen.blit(font.render(f"MAP: {ROADS[road_idx]}", True, (255, 255, 255)), (200, 225))
        screen.blit(font.render(f"GOAL: {dist_val} m", True, (255, 255, 255)), (200, 295))
        screen.blit(font.render(f"DIFF: {DIFFICULTIES[diff_idx]}", True, (255, 255, 255)), (200, 365))

        # Отрисовка всех кнопок из списка
        for b in [btn_next_car, btn_next_road, btn_next_dist, btn_next_diff, btn_save]: 
            b.draw(screen)
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
            
            # Логика циклического переключения индексов через оператор % (остаток от деления)
            if btn_next_car.is_clicked(event): 
                car_idx = (car_idx + 1) % len(CARS)
            
            if btn_next_road.is_clicked(event): 
                road_idx = (road_idx + 1) % len(ROADS)
            
            # Логика выбора дистанции (увеличиваем на 500, сбрасываем после 5000)
            if btn_next_dist.is_clicked(event): 
                dist_val = 500 if dist_val >= 5000 else dist_val + 500
            
            # Переключение сложности (0 -> 1 -> 2 -> 0)
            if btn_next_diff.is_clicked(event):
                diff_idx = (diff_idx + 1) % 3 
                
            # Сохранение и выход
            if btn_save.is_clicked(event):
                # Обновляем словарь настроек новыми значениями
                settings.update({
                    "car_type": CARS[car_idx], 
                    "road_type": ROADS[road_idx], 
                    "finish_distance": dist_val,
                    "difficulty": diff_idx
                })
                # Записываем изменения в физический файл settings.json
                save_settings(settings)
                
                # ВАЖНО: Перезагружаем изображения, чтобы изменения применились сразу
                road_img, car_sprites = update_game_assets() 
                
                return # Выходим из функции настроек обратно в меню
        
        pygame.display.flip()
        clock.tick(60)

def game_over_screen(score, dist, coins, win=False):
    """
    ЭКРАН ОКОНЧАНИЯ ИГРЫ
    Вызывается либо при смерти игрока, либо при достижении дистанции финиша.
    """
    # Сразу сохраняем результат заезда в JSON файл через persistence.py
    save_score(current_user, score, dist, coins)
    
    # Подготовка кнопок для управления после заезда
    # RETRY (перезапуск) и MENU (выход в главное меню)
    btn_retry = Button("RETRY", WIDTH//2 - 210, 450, 200, 60, (46, 204, 113), (39, 174, 96))
    btn_menu = Button("MENU", WIDTH//2 + 10, 450, 200, 60, (41, 128, 185), (31, 97, 141))

    while True:
        # Меняем цвет фона в зависимости от результата:
        # Темно-зеленый при победе (win=True), темно-красный при проигрыше
        screen.fill((0, 40, 0) if win else (50, 0, 0))
        
        # Определяем текст заголовка
        txt = "FINISH REACHED!" if win else "GAME OVER"
        
        # Рендерим крупный заголовок шрифтом Impact
        msg = pygame.font.SysFont("Impact", 80).render(txt, True, (255, 255, 255))
        # Центрируем текст по горизонтали (WIDTH//2 - ширина_текста//2)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 150))
        
        # Отрисовываем кнопки на экране
        for b in [btn_retry, btn_menu]: 
            b.draw(screen)
            
        # Обработка событий ввода
        for event in pygame.event.get():
            # Стандартная проверка на закрытие окна
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
            
            # Если нажата кнопка RETRY, возвращаем True в game_loop, чтобы запустить новый цикл
            if btn_retry.is_clicked(event): 
                return True
            
            # Если нажата кнопка MENU, возвращаем False для выхода в главное меню
            if btn_menu.is_clicked(event): 
                return False
                
        pygame.display.flip() # Обновляем кадр
        clock.tick(60)        # Поддерживаем стабильный FPS


def game_loop():
    """
    ОСНОВНОЙ ИГРОВОЙ ЦИКЛ
    Здесь обрабатывается физика, отрисовка, столкновения и логика уровней.
    """
    # --- Инициализация объектов перед стартом заезда ---
    player = Player(car_sprites)
    
    # Группы спрайтов для удобного управления коллизиями и отрисовкой
    enemies = pygame.sprite.Group() # Вражеские машины
    props = pygame.sprite.Group()   # Препятствия и бонусы (масло, нитро)
    coins = pygame.sprite.Group()   # Монетки
    ui_effects = pygame.sprite.Group() # Вылетающий текст (+1, +5)
    
    # Общая группа для игрока и врагов (для вызова метода update одной строкой)
    all_sprites = pygame.sprite.Group(player)

    # Локальные переменные состояния конкретного заезда
    distance = 0         # Пройденный путь в пикселях
    collected_coins = 0  # Количество собранных монет
    scroll_y = 0         # Смещение фона для эффекта движения
    boost_timer = 0      # Время действия ускорения (мс)
    shield_timer = 0     # Время действия щита (мс)
    
    # 1. Получаем настройки заезда (дистанция и сложность)
    FINISH_DIST = settings.get("finish_distance", 1000) * 10
    diff_level = settings.get("difficulty", 1) # 0: Easy, 1: Medium, 2: Hard
    
    # 2. Настройка сложности (Масштабирование)
    base_speed = 5 + (diff_level * 2) # Базовая скорость выше на Hard
    # Частота появления объектов (на Hard объекты появляются чаще)
    spawn_rate = 1000 - (diff_level * 150) 
    
    # Создаем пользовательское событие для таймера спавна
    SPAWN_TICK = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_TICK, spawn_rate)

    running = True
    while running:
        # Ограничение FPS и получение дельты времени (dt)
        dt = clock.tick(60)
        
        # Расчет текущей скорости: база + бонус от нитро (если активно)
        current_speed = base_speed + (7 if boost_timer > 0 else 0)
        distance += current_speed # Увеличиваем общий пробег
        
        # Уменьшаем время действия активных бонусов
        if boost_timer > 0: boost_timer -= dt
        if shield_timer > 0: shield_timer -= dt
        if player.sliding_timer > 0: player.sliding_timer -= dt

        # Эффект бесконечной дороги: рисуем фон и сдвигаем его по вертикали
        draw_background(screen, road_img, scroll_y, HEIGHT)
        scroll_y = (scroll_y + current_speed) % HEIGHT

        # --- Обработка событий (Events) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
            
            # По тику таймера создаем новый объект на дороге
            if event.type == SPAWN_TICK:
                lane = random.choice(LANES) # Выбор случайной полосы
                r = random.random()
                
                if r < 0.4: # 40% шанс появления врага
                    new_e = Enemy(random.randint(4 + diff_level, 8 + diff_level))
                    enemies.add(new_e); all_sprites.add(new_e)
                elif r < 0.7: # 30% шанс появления монеты
                    val = random.choices([1, 5], [80, 20])[0] # 1 или 5 очков
                    new_c = Coin(lane, val)
                    coins.add(new_c); all_sprites.add(new_c)
                else: # 30% шанс появления спец-предмета
                    p_type = random.choice([0, 2, 5, 6])
                    new_p = Prop("assets/Props/Misc_props (16 x 16).png", p_type, lane)
                    props.add(new_p)

        # --- Логика и Столкновения (Collisions) ---
        
        # 1. Сбор монет (True означает, что монета удалится при касании)
        coin_hits = pygame.sprite.spritecollide(player, coins, True)
        for c in coin_hits:
            collected_coins += c.value
            base_speed += 0.1 # ДИНАМИЧЕСКАЯ СЛОЖНОСТЬ: игра ускоряется от монет
            ui_effects.add(FloatingText(player.rect.centerx, player.rect.top, f"+{c.value}", (255, 215, 0)))

        # 2. Столкновение с предметами (масло, нитро, щит, барьер)
        p_hits = pygame.sprite.spritecollide(player, props, True)
        for p in p_hits:
            if p.type == 0: boost_timer = 5000 # Нитро на 5 сек
            elif p.type == 6: shield_timer = 6000 # Щит на 6 сек
            elif p.type == 2: player.sliding_timer = 2000 # Масло (занос) на 2 сек
            elif p.type == 5: # Барьер (наносит урон, если нет щита)
                if shield_timer <= 0: player.lives -= 1

        # 3. Столкновение с врагами
        if pygame.sprite.spritecollide(player, enemies, True):
            if shield_timer <= 0:
                player.lives -= 1 # Теряем жизнь только если нет щита

        # --- Проверка условий окончания игры ---
        if player.lives <= 0:
            # Если жизней нет, вызываем Game Over. Если игрок нажмет Retry, вернет True.
            if game_over_screen(distance // 10, distance, collected_coins, win=False):
                return game_loop() # Рекурсивный перезапуск заезда
            return # Выход в главное меню

        if distance >= FINISH_DIST:
            # Если доехали до цели, вызываем экран победы
            if game_over_screen(distance // 10, distance, collected_coins, win=True):
                return game_loop()
            return

        # --- Обновление и Отрисовка (Update & Draw) ---
        
        # Обновляем позиции всех объектов (передаем скорость дороги)
        all_sprites.update(current_speed=current_speed)
        props.update(current_speed=current_speed)
        ui_effects.update()

        # Порядок отрисовки: сначала спрайты, потом эффекты сверху
        all_sprites.draw(screen)
        props.draw(screen)
        ui_effects.draw(screen)
        
        # Если щит активен, рисуем вокруг машины синий круг
        if shield_timer > 0:
            pygame.draw.circle(screen, (0, 200, 255), player.rect.center, 50, 3)

        # --- Интерфейс пользователя (UI) ---
        ui_f = pygame.font.SysFont("Arial", 22, bold=True)
        
        # Отрисовка прогресс-бара финиша
        bar_width = 200
        progress = min(distance / FINISH_DIST, 1.0)
        pygame.draw.rect(screen, (50, 50, 50), (WIDTH//2 - 100, 15, bar_width, 15)) # Фон полоски
        pygame.draw.rect(screen, (0, 255, 0), (WIDTH//2 - 100, 15, int(progress * bar_width), 15)) # Заполнение
        
        # Вывод текста (Монеты, Жизни, Цель)
        screen.blit(ui_f.render(f"Coins: {collected_coins}", True, (255, 215, 0)), (10, 10))
        screen.blit(ui_f.render(f"Lives: {player.lives}", True, (255, 50, 50)), (10, 40))
        screen.blit(ui_f.render(f"Goal: {FINISH_DIST//10}m", True, (255, 255, 255)), (WIDTH//2 + 110, 10))

        pygame.display.flip() # Смена буфера кадра (вывод на монитор)

def main_menu():
    """
    ГЛАВНОЕ МЕНЮ: ТОЧКА ВХОДА В ИГРУ.
    Обеспечивает навигацию между игровым процессом, рекордами и настройками.
    """
    # Инициализация кнопок меню. 
    # Параметры: Текст, X, Y, Ширина, Высота, Основной цвет, Цвет при наведении.
    btn_play = Button("START RACE", 50, 220, 260, 55, (41, 128, 185), (31, 97, 141))
    btn_lead = Button("LEADERBOARD", 50, 285, 260, 55, (241, 196, 15), (212, 172, 13))
    btn_sett = Button("SETTINGS", 50, 350, 260, 55, (41, 128, 185), (31, 97, 141))
    btn_exit = Button("EXIT", 50, 415, 260, 55, (192, 57, 43), (146, 43, 33))

    scroll = 0 # Переменная для хранения смещения анимированного фона
    
    while True:
        # ЭФФЕКТ ДВИЖЕНИЯ: Сдвигаем фон вниз на 3 пикселя каждый кадр.
        # Использование % HEIGHT позволяет фону бесконечно "зацикливаться".
        scroll = (scroll + 3) % HEIGHT
        draw_background(screen, road_img, scroll, HEIGHT)
        
        # Отрисовка названия игры с использованием шрифта Impact и золотистого цвета
        title_surf = pygame.font.SysFont("Impact", 80).render("Racer Game", True, (255, 215, 0))
        screen.blit(title_surf, (50, 80))
        
        # Отрисовываем все кнопки меню на текущем кадре
        for b in [btn_play, btn_lead, btn_sett, btn_exit]: 
            b.draw(screen)
        
        # ОБРАБОТКА СОБЫТИЙ МЕНЮ
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
            
            # Если нажата "PLAY": сначала идем на экран ввода имени, потом в саму игру
            if btn_play.is_clicked(event): 
                username_screen() 
                game_loop()
            
            # Переход к таблице рекордов
            if btn_lead.is_clicked(event): 
                leaderboard_screen()
            
            # Переход в меню настроек
            if btn_sett.is_clicked(event): 
                settings_screen()
            
            # Полный выход из приложения
            if btn_exit.is_clicked(event): 
                pygame.quit(); sys.exit()
        
        # Обновляем дисплей для отображения изменений
        pygame.display.flip()
        # Поддерживаем стабильные 60 кадров в секунду (плавность анимации)
        clock.tick(60)

# ТОЧКА ВХОДА В ПРОГРАММУ
# Это условие гарантирует, что меню запустится только при прямом запуске main.py
if __name__ == "__main__":
    main_menu()