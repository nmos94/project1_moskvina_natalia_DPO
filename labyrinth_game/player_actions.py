def get_input(prompt="> "):
    """Безопасно считывает ввод пользователя."""
    try:
        # Считываем текст, убираем пробелы и переводим в нижний регистр
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        # Если пользователь нажал Ctrl+C или Ctrl+D
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    """Отображает предметы, которые игрок несет с собой."""
    inventory = game_state['player_inventory']
    
    print("\n--- ВАША СУМКА ---")
    
    # Проверяем, не пуст ли список
    if not inventory:
        print("Ваш инвентарь пока пуст.")
    else:
        print("У вас с собой:")
        for item in inventory:
            print(f"- {item}")
    
    print("------------------")


from labyrinth_game.constants import ROOMS
import labyrinth_game.utils as utils

def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении, если это возможно."""
    
    # 1. Получаем ID текущей комнаты и её данные
    current_room_id = game_state['current_room']
    room_data = ROOMS[current_room_id]
    
    # 2. Проверяем, есть ли такое направление в словаре exits текущей комнаты
    if direction in room_data['exits']:
        # Находим название новой комнаты
        new_room_id = room_data['exits'][direction]
        
        # 3. Обновляем состояние игры
        game_state['current_room'] = new_room_id
        game_state['steps_taken'] += 1
        
        print(f"\nВы идете на {direction}...")

        # 4. Сразу показываем описание новой комнаты (используем нашу функцию из utils)
        utils.describe_current_room(game_state)
    else:
        # Если направления нет в словаре
        print(f"\nНельзя пойти в этом направлении: {direction}.")

def take_item(game_state, item_name):
    """Позволяет игроку взять предмет из текущей комнаты."""

    # 1. Получаем ID текущей комнаты и её данные
    current_room_id = game_state['current_room']
    room_data = ROOMS[current_room_id]

    # 2. Проверяем, есть ли предмет в списке предметов комнаты
    if item_name in room_data['items']:
        # Добавляем предмет в инвентарь игрока
        game_state['player_inventory'].append(item_name)

        # Удаляем предмет из комнаты
        room_data['items'].remove(item_name)

        print(f"\nВы подняли: {item_name}")
    else:
        # Если предмета нет в комнате
        print("\nТакого предмета здесь нет.")