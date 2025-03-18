import os
import subprocess
from PIL import Image

def convert_png_to_ico(png_path, ico_path):
    """Конвертирует PNG в ICO."""
    try:
        img = Image.open(png_path)
        img.save(ico_path, format="ICO")
        return True
    except Exception as e:
        print(f"Ошибка при конвертации PNG в ICO: {e}")
        return False


def get_file_path(prompt, filetypes):
    """Запрашивает путь к файлу через консоль."""
    while True:
        file_path = input(prompt)
        if os.path.isfile(file_path):
            return file_path
        print("Файл не найден. Попробуйте снова.")


def convert_to_exe():
    """Конвертирует .py файл в .exe с возможностью выбора иконки."""
    # Запрашиваем путь к .py файлу
    print("=== Конвертер .py в .exe ===")
    py_file_path = get_file_path(
        "Введите путь к .py файлу: ",
        filetypes=[("Python files", "*.py")]
    )

    # Получаем имя файла без расширения
    file_name = os.path.splitext(os.path.basename(py_file_path))[0]

    # Запрашиваем новое имя для .exe файла
    new_name = input(
        "Введите новое имя для .exe файла (оставьте пустым, чтобы оставить текущее имя): "
    ).strip()
    if not new_name:
        new_name = file_name

    # Запрашиваем путь к иконке
    use_icon = input("Хотите добавить иконку? (y/n): ").strip().lower()
    icon_option = ""
    if use_icon == "y":
        icon_path = get_file_path(
            "Введите путь к иконке (.ico или .png): ",
            filetypes=[("Icon files", "*.ico"), ("PNG files", "*.png")]
        )
        # Если выбрана .png, конвертируем в .ico
        if icon_path.lower().endswith('.png'):
            ico_path = os.path.splitext(icon_path)[0] + ".ico"
            if convert_png_to_ico(icon_path, ico_path):
                icon_path = ico_path
            else:
                return  # Если конвертация не удалась, выходим
        icon_option = f'--icon="{icon_path}"'

    # Определяем путь для сохранения .exe файла
    output_dir = os.path.dirname(py_file_path)

    # Команда для PyInstaller
    command = f'pyinstaller --onefile --noconsole {icon_option} --distpath "{output_dir}" --name "{new_name}" "{py_file_path}"'

    print("\n=== Начало конвертации ===")
    try:
        # Запускаем PyInstaller
        subprocess.run(command, shell=True, check=True)
        print(f"Файл {new_name}.exe успешно создан в папке: {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации: {e}")
    except FileNotFoundError:
        print("PyInstaller не найден. Установите его с помощью 'pip install pyinstaller'.")


if __name__ == "__main__":
    convert_to_exe()
