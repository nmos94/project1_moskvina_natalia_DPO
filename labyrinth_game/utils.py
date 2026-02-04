# labyrinth_game/utils.py
from labyrinth_game.constants import ROOMS
import labyrinth_game.player_actions as actions

def show_help():
    """Выводит список доступных команд."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

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

def attempt_open_treasure(game_state):
    """Реализует логику победы - открытие сундука с сокровищами."""

    # 1. Получаем данные комнаты
    current_room_id = game_state['current_room']
    room_data = ROOMS[current_room_id]

    # 2. Проверяем, есть ли у игрока ключ от сокровищницы
    if 'treasure_key' in game_state['player_inventory']:
        # У игрока есть ключ - открываем сундук
        print("\nВы применяете ключ, и замок щёлкает. Сундук открыт!")

        # Удаляем сундук из комнаты
        if 'treasure_chest' in room_data['items']:
            room_data['items'].remove('treasure_chest')

        # Объявляем победу
        print("\nВ сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    # 3. Если ключа нет - предлагаем ввести код
    print("\nСундук заперт. Вы можете попытаться взломать его, введя код.")
    choice = actions.get_input("Ввести код? (да/нет): ")

    if choice == "да":
        # Игрок хочет попробовать ввести код
        # Проверяем, есть ли загадка (код) для этой комнаты
        if room_data.get('puzzle'):
            puzzle_question, correct_answer = room_data['puzzle']

            # Запрашиваем код
            code = actions.get_input("Введите код: ")

            # Проверяем код
            if code.lower() == correct_answer.lower():
                # Код верный
                print("\n✓ Код верный! Замок открывается!")

                # Удаляем сундук из комнаты
                if 'treasure_chest' in room_data['items']:
                    room_data['items'].remove('treasure_chest')

                # Убираем загадку
                room_data['puzzle'] = None

                # Объявляем победу
                print("\nВ сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                # Код неверный
                print("\nНеверный код. Сундук остается запертым.")
        else:
            print("\nНет системы для ввода кода.")
    else:
        # Игрок отказался вводить код
        print("\nВы отступаете от сундука.")

def solve_puzzle(game_state):
    """Позволяет игроку решить загадку в текущей комнате."""

    # 1. Получаем ID текущей комнаты и её данные
    current_room_id = game_state['current_room']
    room_data = ROOMS[current_room_id]

    # 2. Особый случай: если мы в treasure_room и есть treasure_chest
    if current_room_id == 'treasure_room' and 'treasure_chest' in room_data['items']:
        attempt_open_treasure(game_state)
        return

    # 3. Проверяем, есть ли загадка в комнате
    if not room_data.get('puzzle'):
        print("\nЗагадок здесь нет.")
        return

    # 4. Получаем данные загадки (вопрос и правильный ответ)
    puzzle_question, correct_answer = room_data['puzzle']

    # 5. Выводим вопрос
    print(f"\n{puzzle_question}")

    # 6. Получаем ответ от пользователя
    user_answer = actions.get_input("Ваш ответ: ")

    # 7. Сравниваем ответ (приводим к нижнему регистру для сравнения)
    if user_answer.lower() == correct_answer.lower():
        # Ответ верный
        print("\n✓ Правильно! Загадка решена!")

        # Убираем загадку из комнаты (чтобы нельзя было решить дважды)
        room_data['puzzle'] = None

        # Добавляем награду игроку
        print("Вы получаете награду за решение загадки!")
    else:
        # Ответ неверный
        print("\nНеверно. Попробуйте снова.")