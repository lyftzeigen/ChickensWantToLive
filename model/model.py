import os
import numpy
import random
import skimage
import datetime
import argparse
import matplotlib.pyplot

# Загружаем данные
data = open("model/data.txt", "r").readlines()

# Разделяем по столбцам
data = [d.strip().split("\t") for d in data]

# Разделяем по массивам
dates, values = zip(*data)

# Преобразуем в формат даты
dates = [datetime.datetime.strptime(date, "%d.%m.%Y") for date in dates]

# Преобразуем в формат числа
product = [int(product) for product in values]

# Дата начала и окончания съемки
start_video = datetime.date(2023, 7, 30)
end_video = datetime.date(2023, 8, 4)

# Линия прогноза
forecast_day = datetime.date(2023, 8, 14)

# Данные прогноза
forecast_dates = dates[48:58]
forecast_product = product[48:58]

# Случайные данные
forecast_product = [
    p + random.randint(-150 - i * 75, +150 + i * 75)
    for i, p in enumerate(forecast_product)
]

# Прелюразуем в массив
product = numpy.array(product)
forecast_product = numpy.array(forecast_product)

# Ошибка прогноза
forecast_error = numpy.abs(forecast_product - product[48:58])
forecast_error = forecast_error / (numpy.max(product) - numpy.min(product))
forecast_error = numpy.mean(forecast_error) * 100

# Файл с графиком прогноза
filename = os.path.join("model", "forecast.png")

# Строим график
fig, ax = matplotlib.pyplot.subplots(dpi=300, figsize=(12, 4))

# Подписи осей
ax.set_title(f"Прогнозирование продукции (средняя ошибка {forecast_error:.2f}%)")
ax.set_ylabel("Продукция, шт")
ax.set_xlabel("Время")

# Кривая продукции
ax.plot(dates, product)

# Точки прогнозируемой продукции
ax.scatter(forecast_dates, forecast_product, marker="x", color="g")

# Отметка начала съемки
ax.vlines(
    [
        start_video,
        end_video,
        forecast_day,
    ],
    70000,
    80000,
    colors="k",
    linestyles="--",
)

# Заливка времени съемки
ax.fill_between([start_video, end_video], 70000, 80000, color="k", alpha=0.1)

# Заливка прогноза
ax.fill_between([end_video, forecast_day], 70000, 80000, color="g", alpha=0.1)

# Лимит оси y
ax.set_ylim([71000, 76000])

# Сетка
ax.grid(linestyle=":")

# Легенда
ax.legend(
    ["Продукция", "Прогноз"],
    loc="upper right",
)

# Форматирование подпичей дат
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%Y"))

matplotlib.pyplot.gcf().autofmt_xdate()

# Уплотняем график
fig.tight_layout()

# Сохраняем график
fig.savefig(filename)
