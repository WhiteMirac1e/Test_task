import requests
from time import time


# Функция для добавления заметки
def add_note(url, data):
    response = requests.post(url, json=data)
    return response.status_code


# Функция для удаления заметки
def delete_note(url, id):
    response = requests.delete(f"{url}/{id}")
    return response.status_code


# Функция для тестирования производительности
def test_performance(url, num_operations, ratio):
    # Инициализация времени начала теста
    start_time = time()

    # Генерируем случайные данные для заметок
    notes_data = []
    for _ in range(num_operations):
        note = {
            "note": "Пример заметки",
            "description": "Описание заметки"
        }
        notes_data.append(note)

    # Эмуляция добавления заметок
    added_count = 0
    for note in notes_data:
        if add_note(url, note) == 201:
            added_count += 1

    print("Добавлено заметок:", added_count)

    # Эмуляция удаления заметок
    deleted_count = int(ratio * added_count) if ratio else 0

    for i in range(deleted_count):
        id = notes_data[i % added_count]["id"]
        if delete_note(url, str(id)) == 204:
            deleted_count -= 1

    print("Удалено заметок:", deleted_count)

    # Вычисление общего времени выполнения теста
    end_time = time()
    total_time = end_time - start_time

    # Вывод результатов теста
    print(f"Общее время выполнения: {total_time}, секунд")
    print("Средняя скорость добавления заметок:", added_count / total_time)
    print("Средняя скорость удаления заметок:", deleted_count / total_time)


# Ввод параметров теста
url = input("Введите URL сервера: ")
num_operations = int(input("Введите количество операций: "))
ratio = float(input("Введите соотношение операций добавления к удалению (или оставьте пустым для отсутствия удаления): "))

# Запуск теста
test_performance(url, num_operations, ratio)
