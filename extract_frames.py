import os
import shutil
import asyncio
import argparse


# Парсер аргументов командной строки
parser = argparse.ArgumentParser(description="🐓 VideoFrameExtractor")

# Добавляем аргумент директории
parser.add_argument(
    "directory",
    type=str,
    help="Директория с видео-файлами - remuxed/{directory}",
)

parser.add_argument(
    "frames",
    type=int,
    help="Количество кадров для извлечения",
)

# Получаем аргументы
args = parser.parse_args()

print("🐓 VideoFrameExtractor\n")

# Очистим директорию от файлов
if os.path.isdir(os.path.join("frames", args.directory)):
    shutil.rmtree(os.path.join("frames", args.directory))

# Создадим директории, если их нет
for directory in ["remuxed", "frames"]:
    if not os.path.isdir(os.path.join(directory, args.directory)):
        os.makedirs(os.path.join(directory, args.directory))

print(f"🚀 Извлечение кадров из 'remuxed/{args.directory}'...\n")

# Извлечение кадра
async def extract_frame(semaphore):
    async with semaphore:
        process = await asyncio.create_subprocess_exec(
            "python3",
            "extract_random_frame.py",
            args.directory,
        )

        await process.wait()


# Точка входа в контексте asyncio
async def main():
    # Ограничиваем количество одновременных задач
    semaphore = asyncio.Semaphore(16)

    # Формируем задачи
    tasks = [asyncio.create_task(extract_frame(semaphore)) for _ in range(args.frames)]

    # Запускаем задачи
    await asyncio.gather(*tasks)


asyncio.run(main())

print("\n🥵 Готово! Ох, это было не просто...")
