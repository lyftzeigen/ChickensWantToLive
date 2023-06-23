import os
import argparse
import ultralytics
from tqdm import tqdm

# Парсер аргументов командной строки
parser = argparse.ArgumentParser(description="🐓 YOLOv8VideoProcessing")

# Добавляем аргумент директории
parser.add_argument(
    "directory",
    type=str,
    help="Директория с видео файлами - remux/{directory}",
)

# Получаем аргументы
args = parser.parse_args()

print("🐓 YOLOv8VideoProcessing\n")

# Создадим директории, если их нет
if not os.path.isdir(os.path.join("processing", args.directory)):
    os.makedirs(os.path.join("processing", args.directory))

if not os.path.isdir(os.path.join("remuxed", args.directory)):
    os.makedirs(os.path.join("remuxed", args.directory))

# Путь к весам модели
weights = os.path.join("training", "take", "weights", "best.engine")

# Завершение работы при отсутствии весов
if not os.path.exists(weights):
    print(f"😡 Весов модели не обнаружено - {weights}")
    exit()

# Загружаем модель
model = ultralytics.YOLO(weights, task="detect")

# Путь к директории с видео-файлами
folder = os.path.join("remuxed", args.directory, "*.mp4")

# Подготавливаем модель для потоковой обработки
predict = model.predict(
    folder,
    imgsz=640,
    conf=0.3,
    stream=True,
    save=False,
    show_labels=False,
    show_conf=False,
    verbose=False,
)

# Файл с количеством детекций для каждого кадра
detections = os.path.join("processing", args.directory, "detections.txt")

# Открываем файл и записываем в него результаты детекции
with open(detections, "w") as file:
    print(f"\nЗапись обработанных данных в файл '{detections}'\n")
    for r in tqdm(predict):
        file.write(f"{len(r.boxes)}\n")
