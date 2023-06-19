import os
import shutil
import ultralytics

print("🐓 YOLOv8Trainer\n")

# Очищаем конфигурацию YOLOv8
os.remove(os.path.join(os.path.expanduser("~"), ".config/Ultralytics/settings.yaml"))

# Очищаем директорию training
if os.path.exists("training"):
    shutil.rmtree("training")
    os.makedirs("training")

# Загружаем предобученную модель
model = ultralytics.YOLO(os.path.join("weights", "yolov8n.pt"))

# Запукаем обучение модели
model.train(
    batch=16,
    epochs=100,
    imgsz=640,
    data=os.path.join("datasets", "data.yaml"),
    project="training",
    name="take",
)

# Экспортируем в формат TensorRT
model.export(
    format="engine",
    device=0,
    verbose=False,
)

print("\n🥵 Готово!")
