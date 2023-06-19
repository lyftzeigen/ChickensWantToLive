import os
import glob
import ffmpeg
import argparse

# Парсер аргументов командной строки
parser = argparse.ArgumentParser(description="🐓 HikvisionCameraRemux")

# Добавляем аргумент директории
parser.add_argument(
    "directory",
    type=str,
    help="Директория с видео файлами - videos/{directory}",
)

# Получаем аргументы
args = parser.parse_args()

print("🐓 HikvisionCameraRemux\n")

# Создадим директории, если их нет
if not os.path.isdir("videos"):
    os.makedirs("videos")

if not os.path.isdir(os.path.join("remuxed", args.directory)):
    os.makedirs(os.path.join("remuxed", args.directory))

# Получаем все файлы из запрашиваемой директории
source_files = sorted(glob.glob(os.path.join("videos", args.directory, "*.mp4")))

for file_path in source_files:
    try:
        print(f"📹 Обработка видео-файла '{file_path}'")

        # Получаем имя файла
        base_name = os.path.basename(file_path)

        # Получаем свойства видео-файла
        probe = ffmpeg.probe(file_path)

        # Извлекаем продолжительность видео
        duration = probe["streams"][0]["duration"]

        # Выводим информацию о файле
        print(f"   Продолжительность: {int(float(duration))} с")

        # Параметры копирования видео потока
        output_parameters = {
            "c:v": "copy",
            "y": None,
            "hide_banner": None,
            "loglevel": "error",
        }

        # Путь выходного файла
        output_filename = os.path.join("remuxed", args.directory, base_name)

        # Преобразуем файл
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.output(stream, output_filename, **output_parameters)
        stream.run()

        # Находим размер нового видео
        file_size = os.path.getsize(output_filename)

        # Выводим информацию
        print(f"   Размер: {file_size:,} байт")
        print("😊 Готово\n")

    except ffmpeg.Error as e:
        print(f"\n\nAn error occurred: {e.stderr.decode('utf-8')}")
