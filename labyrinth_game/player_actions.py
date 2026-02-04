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

        # 2.1. Проверка доступа в treasure_room
        if new_room_id == 'treasure_room' and 'rusty_key' not in game_state['player_inventory']:
            print("\nДверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

        # 2.2. Если переходим в treasure_room с ключом
        if new_room_id == 'treasure_room' and 'rusty_key' in game_state['player_inventory']:
            print("\nВы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")

        # 3. Обновляем состояние игры
        game_state['current_room'] = new_room_id
        game_state['steps_taken'] += 1

        print(f"\nВы идете на {direction}...")

        # 4. Сразу показываем описание новой комнаты (используем нашу функцию из utils)
        utils.describe_current_room(game_state)

        # 5. Вызываем случайное событие после перемещения
        utils.random_event(game_state)
    else:
        # Если направления нет в словаре
        print(f"\nНельзя пойти в этом направлении: {direction}.")

def take_item(game_state, item_name):
    """Позволяет игроку взять предмет из текущей комнаты."""

    # 1. Проверяем особый случай: попытка взять сундук с сокровищами
    if item_name == 'treasure_chest':
        print("\nВы не можете поднять сундук, он слишком тяжелый.")
        return

    # 2. Получаем ID текущей комнаты и её данные
    current_room_id = game_state['current_room']
    room_data = ROOMS[current_room_id]

    # 3. Проверяем, есть ли предмет в списке предметов комнаты
    if item_name in room_data['items']:
        # Добавляем предмет в инвентарь игрока
        game_state['player_inventory'].append(item_name)

        # Удаляем предмет из комнаты
        room_data['items'].remove(item_name)

        print(f"\nВы подняли: {item_name}")
    else:
        # Если предмета нет в комнате
        print("\nТакого предмета здесь нет.")

def use_item(game_state, item_name):
    """Использует предмет из инвентаря игрока."""

    # Проверяем, есть ли предмет в инвентаре
    if item_name not in game_state['player_inventory']:
        print("\nУ вас нет такого предмета.")
        return

    # Выполняем действие в зависимости от предмета
    match item_name:
        case "torch":
            print("\nВы зажигаете факел. Вокруг стало намного светлее!")

        case "sword":
            print("\nВы крепче сжимаете рукоять меча. Вы чувствуете уверенность и готовность к бою!")

        case "bronze_box":
            print("\nВы открываете бронзовую шкатулку...")
            # Проверяем, нет ли уже ключа в инвентаре
            if 'rusty_key' not in game_state['player_inventory']:
                game_state['player_inventory'].append('rusty_key')
                print("Внутри вы находите ржавый ключ!")
            else:
                print("Шкатулка пуста.")

        case _:
            # Для всех остальных предметов
            print(f"\nВы не знаете, как использовать {item_name}.")