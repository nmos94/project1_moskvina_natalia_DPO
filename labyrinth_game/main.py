# labyrinth_game/main.py
from labyrinth_game.constants import ROOMS
import labyrinth_game.player_actions as actions
import labyrinth_game.utils as utils

# 1. Состояние игры
game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def main():
    # 2. Приветствие
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    # 3. Описание стартовой комнаты (вызываем функцию из utils)
    utils.describe_current_room(game_state)
    
    # 4. Основной игровой цикл
    while not game_state['game_over']:
        # Используем нашу новую функцию из модуля actions
        command = actions.get_input("\nЧто вы будете делать? > ")
        
        # Обрабатываем команду выхода (включая "quit" из нашей новой функции)
        if command in ["exit", "выход", "quit"]:
            print("Спасибо за игру!")
            game_state['game_over'] = True
            
        elif command == "inventory":
            actions.show_inventory(game_state)
            
        elif command == "look":
            utils.describe_current_room(game_state)
            
        else:
            print("Неизвестная команда. Попробуйте 'look', 'inventory' или 'exit'.")

# 5. Стандартная конструкция запуска
if __name__ == "__main__":
    main()