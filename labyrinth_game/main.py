# labyrinth_game/main.py
import labyrinth_game.player_actions as actions
import labyrinth_game.utils as utils

# 1. Состояние игры
game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0,
    'puzzles_solved': 0,
    'bronze_box_opened': False
}

def process_command(game_state, command):
    """Обрабатывает команды игрока и вызывает соответствующие функции."""

    # Разделяем строку на части: команда и аргумент(ы)
    parts = command.split()

    # Если строка пустая, игнорируем
    if not parts:
        print("Вы ничего не ввели.")
        return

    # Первое слово — это команда
    cmd = parts[0]

    # Остальные слова — аргументы (если есть)
    args = parts[1:] if len(parts) > 1 else []

    # Используем match/case для обработки команд
    match cmd:
        case "look":
            # Показать описание текущей комнаты
            utils.describe_current_room(game_state)

        case "go":
            # Переместиться в указанном направлении
            if args:
                direction = args[0]
                actions.move_player(game_state, direction)
            else:
                print("Укажите направление (north, south, east, west).")

        case "north" | "south" | "east" | "west":
            # Односложные команды направлений
            actions.move_player(game_state, cmd)

        case "take":
            # Взять предмет
            if args:
                item_name = args[0]
                actions.take_item(game_state, item_name)
            else:
                print("Укажите название предмета, который хотите взять.")

        case "inventory" | "inv":
            # Показать инвентарь
            actions.show_inventory(game_state)

        case "quit" | "exit":
            # Выход из игры
            print("Спасибо за игру!")
            game_state['game_over'] = True

        case "use":
            # Использовать предмет
            if args:
                item_name = args[0]
                actions.use_item(game_state, item_name)
            else:
                print("Укажите, что вы хотите использовать.")

        case "solve":
            # Решить загадку или открыть сокровищницу
            current_room_id = game_state['current_room']
            if current_room_id == 'treasure_room':
                # В treasure_room команда solve открывает сундук
                utils.attempt_open_treasure(game_state)
            else:
                # В других комнатах решаем загадки
                utils.solve_puzzle(game_state)

        case "help":
            # Показать справку
            utils.show_help()

        case _:
            # Неизвестная команда
            print("Неизвестная команда. Используйте 'help' для списка команд.")

def main():
    # 2. Приветствие
    print("Добро пожаловать в Лабиринт сокровищ!")
    print("\n💡 Подсказка: введите 'help' для просмотра всех команд\n")

    # 3. Описание стартовой комнаты (вызываем функцию из utils)
    utils.describe_current_room(game_state)

    # 4. Основной игровой цикл
    while not game_state['game_over']:
        # Получаем команду от пользователя
        command = actions.get_input("\nЧто вы будете делать? > ")

        # Обрабатываем команду через нашу функцию
        process_command(game_state, command)

# 5. Стандартная конструкция запуска
if __name__ == "__main__":
    main()