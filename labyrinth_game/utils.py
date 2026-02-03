# labyrinth_game/utils.py
from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    """Выводит полную информацию о комнате, в которой находится игрок."""
    
    # 1. Находим имя текущей комнаты из состояния игры
    room_id = game_state['current_room']
    
    # 2. Берем данные этой комнаты из нашего большого словаря ROOMS
    room_data = ROOMS[room_id]
    
    # 3. Выводим название в верхнем регистре (метод .upper())
    print(f"\n== {room_id.upper()} ==")
    
    # 4. Выводим описание
    print(room_data['description'])
    
    # 5. Выводим предметы, если список не пуст
    if room_data['items']:
        # join склеит список в строку через запятую
        items_str = ", ".join(room_data['items'])
        print(f"Заметные предметы: {items_str}")
        
    # 6. Выводим доступные выходы (берем ключи из словаря exits)
    exits = ", ".join(room_data['exits'].keys())
    print(f"Выходы: {exits}")
    
    # 7. Проверяем наличие загадки
    if room_data.get('puzzle'):
        print("Кажется, здесь есть загадка (используйте команду solve).")