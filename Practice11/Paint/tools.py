import pygame

def flood_fill(surface, start_pos, fill_color):
    """Алгоритм заливки области цветом."""
    try:
        target_color = surface.get_at(start_pos)
    except IndexError:
        return
        
    if target_color == fill_color:
        return
        
    w, h = surface.get_size()
    # Используем список как очередь для BFS
    q = [start_pos]
    
    while q:
        x, y = q.pop(0)
        if 0 <= x < w and 0 <= y < h:
            if surface.get_at((x, y)) == target_color:
                surface.set_at((x, y), fill_color)
                # Добавляем соседей
                q.append((x + 1, y))
                q.append((x - 1, y))
                q.append((x, y + 1))
                q.append((x, y - 1))

def get_rect(start_pos, end_pos):
    """Возвращает корректный объект Rect независимо от направления движения мыши."""
    x = min(start_pos[0], end_pos[0])
    y = min(start_pos[1], end_pos[1])
    w = abs(start_pos[0] - end_pos[0])
    h = abs(start_pos[1] - end_pos[1])
    return pygame.Rect(x, y, w, h)

def get_distance(p1, p2):
    """Вычисляет расстояние между двумя точками (радиус)."""
    return int(((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5)