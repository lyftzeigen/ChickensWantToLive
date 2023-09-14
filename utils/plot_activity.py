import os
import numpy
import skimage
import datetime
import argparse
import matplotlib.pyplot


# Парсер аргументов командной строки
parser = argparse.ArgumentParser(description="🐓 ActivityPlot")

# Добавляем аргумент директории
parser.add_argument(
    "directory",
    type=str,
    help="Директория с детекциями/{directory}",
)

# Получаем аргументы
args = parser.parse_args()

print("🐓 ActivityPlot\n")

# Создадим директории, если их нет
if not os.path.isdir(os.path.join("processing", args.directory)):
    os.makedirs(os.path.join("processing", args.directory))

print(f"🚀 Чтение даных 'procerssing/{args.directory}'...\n")

# Файл с детекциями
filename = os.path.join("processing", args.directory, "detections.txt")

# Проверка наличия файла
if not os.path.isfile(filename):
    print(f"😡 Файл отсутствует '{filename}'...\n")
    exit()

# Чтение данных
data = []

with open(filename, "r") as file:
    data = [int(row) for row in file.readlines()]

# Параметры обработки данных (временное окно и частота кадров видео)
time_interval = 30
frames_per_second = 30

# Разделяем данные на порции согласно временному окну
split_data = numpy.array_split(data, len(data) // (frames_per_second * time_interval))

# Реальное время начала съемки
start_date_time = datetime.datetime(2023, 7, 30, 10, 30, 0)

# Временные интервалы для отображения на графике
split_data_timestamps = [
    start_date_time + datetime.timedelta(seconds=td * time_interval)
    for td in range(len(split_data))
]

# Характеристики активности для каждой порции данных
split_data_median = numpy.array([numpy.median(batch) for batch in split_data]) * 1.0
split_data_median_plus = numpy.array([numpy.max(batch) for batch in split_data]) * 1.0
split_data_median_minus = numpy.array([numpy.min(batch) for batch in split_data]) * 1.0

# Сглаживаем данные для презентативного вида
split_data_median = skimage.filters.gaussian(split_data_median, 2)
split_data_median_plus = skimage.filters.gaussian(split_data_median_plus, 2)
split_data_median_minus = skimage.filters.gaussian(split_data_median_minus, 2)

# Расчет временных параметров
frames = len(data)
seconds = frames // 30
hours = seconds // 3600
minutes = (seconds % 3600) // 60
seconds = (seconds % 3600) % 60

fig, ax = matplotlib.pyplot.subplots(dpi=300, figsize=(20, 5))

ax.set_title(f"Активность птицы за {hours:02d}:{minutes:02d}:{seconds:02d}")
ax.set_ylabel("Активность")
ax.set_xlabel("Время")

ax.plot(
    split_data_timestamps,
    split_data_median,
    color="green",
)

ax.plot(
    split_data_timestamps,
    split_data_median_plus,
    color="red",
    alpha=0.25,
    linestyle="--",
)

ax.plot(
    split_data_timestamps,
    split_data_median_minus,
    color="blue",
    alpha=0.25,
    linestyle="--",
)

ax.fill_between(
    split_data_timestamps,
    split_data_median_plus,
    split_data_median_minus,
    color="blue",
    alpha=0.1,
)

ax.set_xlim([split_data_timestamps[0], split_data_timestamps[-1]])

ax.grid(linestyle=":")

ax.legend(
    [
        "Медиана активности",
        "Максимальная активность",
        "Минимальная активность",
    ],
    loc="upper right",
)

ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1 / 24 / 2))
ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1 / 24 / 12))
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))

matplotlib.pyplot.gcf().autofmt_xdate()

# Файл с графиком активности
filename = os.path.join("processing", args.directory, "activity.png")

# Уплотняем график
fig.tight_layout()

# Сохраняем график
fig.savefig(filename)

print(f"🥵 Готово! Активность курочек можно посмотреть в файле '{filename}'")
