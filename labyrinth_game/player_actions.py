def get_input(prompt="> "):
    """Безопасно считывает ввод пользователя."""
    try:
        # Считываем текст, убираем пробелы и переводим в нижний регистр
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        # Если пользователь нажал Ctrl+C или Ctrl+D
        print("\nВыход из игры.")
        return "quit"

# Твоя предыдущая функция show_inventory остается ниже...