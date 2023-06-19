import os
import uuid
import glob
import ffmpeg
import random
import argparse

# Парсер аргументов командной строки
parser = argparse.ArgumentParser(description="🐓 VRandomFrameExtractor")

# Добавляем аргумент директории
parser.add_argument(
    "directory",
    type=str,
    help="Директория с видео-файлами - remuxed/{directory}",
)

# Получаем аргументы
args = parser.parse_args()

# Получаем список всех видео файлов
files = glob.glob(os.path.join("remuxed", args.directory, "*.mp4"))

# Берем случайный файл
video_path = random.choice(files)

# Получаем свойства видео-файла
probe = ffmpeg.probe(video_path)

# Получаем длительность видео-файла
duration = int(float(probe["streams"][0]["duration"]))

# Получаем случайное время кадра
frame_time = random.randint(0, duration)

# Получаем случайное имя файла с кадром
frame_path = os.path.join(
    "frames",
    args.directory,
    f"{uuid.uuid4().hex[:8]}.jpg",
)

output_parameters = {
    "vframes": 1,
    "y": None,
    "hide_banner": None,
    "loglevel": "error",
}

# Извлекаем кадр
stream = ffmpeg.input(video_path, ss=frame_time)
stream = stream.output(frame_path, **output_parameters)
stream.run()

# Получаем только имена файлов
video_name = os.path.basename(video_path)
frame_name = os.path.basename(frame_path)

print(f"   Извлечен кадр '{frame_name}' из файла '{video_name}'")
