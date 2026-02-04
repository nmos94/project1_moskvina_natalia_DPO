
import math

import labyrinth_game.player_actions as actions
from labyrinth_game.constants import COMMANDS, ROOMS


def pseudo_random(seed, modulo):
    """Генерирует псевдослучайное число в диапазоне [0, modulo)."""
    # Берем синус от seed, умноженного на большое число с дробной частью
    sine_value = math.sin(seed * 12.9898)

    # Умножаем на другое большое число
    large_value = sine_value * 43758.5453

    # Получаем дробную часть
    fractional_part = large_value - math.floor(large_value)

    # Приводим к диапазону [0, modulo) и возвращаем целое число
    return int(fractional_part * modulo)

def trigger_trap(game_state):
    """Имитирует срабатывание ловушки с негативными последствиями."""
    print("\nЛовушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    if inventory:
        # Если инвентарь не пуст, удаляем случайный предмет
        random_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(random_index)
        print(f"В суматохе вы потеряли предмет: {lost_item}!")
    else:
        # Если инвентарь пуст, игрок получает урон
        damage_roll = pseudo_random(game_state['steps_taken'], 10)

        if damage_roll < 3:
            # Критический урон - поражение
            print("Ловушка оказалась смертельной...")
            print("\n=== GAME OVER ===")
            print("Вы погибли от ловушки.")
            game_state['game_over'] = True
        else:
            # Игрок уцелел
            print("Вам удалось уклониться! Вы уцелели, но были напуганы.")

def random_event(game_state):
    """Генерирует случайные события во время перемещения."""
    # Определяем, произойдет ли событие (вероятность 1/10)
    event_chance = pseudo_random(game_state['steps_taken'], 10)

    if event_chance == 0:
        # Выбираем, какое событие произойдет
        event_type = pseudo_random(game_state['steps_taken'] + 1, 3)

        current_room_id = game_state['current_room']
        room_data = ROOMS[current_room_id]

        if event_type == 0:
            # Сценарий 1: Находка
            print("\n✨ Вы замечаете что-то блестящее на полу - это монетка!")
            room_data['items'].append('coin')

        elif event_type == 1:
            # Сценарий 2: Испуг
            print("\n👻 Вы слышите странный шорох в темноте...")
            if 'sword' in game_state['player_inventory']:
                print("Вы хватаетесь за меч и отпугиваете неведомое существо!")
            else:
                print("Вам становится не по себе...")
                print("(Это было случайное событие, можно продолжать)")

        elif event_type == 2:
            # Сценарий 3: Ловушка в trap_room без факела
            if (current_room_id == 'trap_room' and
                    'torch' not in game_state['player_inventory']):
                print("\n⚠️  Без света вы не заметили ловушку!")
                trigger_trap(game_state)

def show_help():
    """Выводит список доступных команд."""
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        # Форматируем команду с выравниванием слева и дополнением
        # пробелами до 16 символов
        print(f"  {command:<16} - {description}")

def _show_victory_stats(game_state):
    """Показывает финальную статистику при победе."""
    print("\n" + "="*40)
    print("           🏆 ПОБЕДА! 🏆")
    print("="*40)
    print(f"Шагов сделано: {game_state['steps_taken']}")
    print(f"Предметов собрано: {len(game_state['player_inventory'])}")
    print(f"Загадок решено: {game_state.get('puzzles_solved', 0)}")

    # Определяем ранг на основе количества шагов
    steps = game_state['steps_taken']
    if steps < 20:
        rank = "⭐⭐⭐ Легенда Лабиринта"
    elif steps < 40:
        rank = "⭐⭐ Мастер Лабиринта"
    elif steps < 60:
        rank = "⭐ Искатель Приключений"
    else:
        rank = "Начинающий Исследователь"

    print(f"Ранг: {rank}")
    print("="*40)

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

        # Объявляем победу с финальной статистикой
        print("\nВ сундуке сокровище!")
        _show_victory_stats(game_state)
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

                # Увеличиваем счетчик решенных загадок (за взлом кода)
                game_state['puzzles_solved'] = (
                    game_state.get('puzzles_solved', 0) + 1
                )

                # Объявляем победу с финальной статистикой
                print("\nВ сундуке сокровище!")
                _show_victory_stats(game_state)
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

    # 4.1. Альтернативные варианты ответов
    alternative_answers = {
        '10': ['десять', 'ten'],
        'шаг шаг шаг': ['шаг-шаг-шаг', 'шагшагшаг'],
        'елка': ['ёлка', 'ель'],
        'резонанс': ['огонь', 'пожар']  # "что растет, когда его съедают"
    }

    # 5. Выводим вопрос
    print(f"\n{puzzle_question}")

    # 6. Получаем ответ от пользователя
    user_answer = actions.get_input("Ваш ответ: ")

    # 7. Проверяем ответ (с учетом альтернатив)
    correct_answer_lower = correct_answer.lower()
    user_answer_lower = user_answer.lower()

    # Создаем список всех правильных вариантов
    valid_answers = [correct_answer_lower]
    if correct_answer_lower in alternative_answers:
        valid_answers.extend([
            alt.lower()
            for alt in alternative_answers[correct_answer_lower]
        ])

    if user_answer_lower in valid_answers:
        # Ответ верный
        print("\n✓ Правильно! Загадка решена!")

        # Убираем загадку из комнаты (чтобы нельзя было решить дважды)
        room_data['puzzle'] = None

        # Увеличиваем счетчик решенных загадок
        game_state['puzzles_solved'] = (
            game_state.get('puzzles_solved', 0) + 1
        )

        # Награда зависит от комнаты
        if current_room_id == 'hall':
            print(
                "Сундук на пьедестале открывается! "
                "Внутри лежит золотой медальон."
            )
            game_state['player_inventory'].append('golden_medallion')
            print("→ Медальон добавлен в вашу сумку.")
        elif current_room_id == 'library':
            print(
                "Полка сдвигается, открывая тайник! "
                "Вы находите магический свиток."
            )
            game_state['player_inventory'].append('magic_scroll')
            print("→ Свиток добавлен в вашу сумку.")
        elif current_room_id == 'trap_room':
            print("Плиты перестали двигаться. Путь безопасен!")
        elif current_room_id == 'dungeon_corridor':
            print("Стена открывается, и вы находите серебряное кольцо!")
            game_state['player_inventory'].append('silver_ring')
            print("→ Кольцо добавлено в вашу сумку.")
        else:
            print("Вы получаете награду за решение загадки!")
    else:
        # Ответ неверный
        print("\nНеверно. Попробуйте снова.")

        # Особая логика для trap_room
        if current_room_id == 'trap_room':
            print("Неправильный ответ активирует ловушку!")
            trigger_trap(game_state)