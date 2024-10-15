import sqlite3
import time
import json
from random import randint, uniform
from flask import Flask, request, render_template, redirect
from __init__ import block_sort  # Импортируем функцию сортировки

# Настройка приложения Flask
app = Flask(__name__)

# Создание базы данных и таблицы
def init_db():
    conn = sqlite3.connect('arrays.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS arrays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_array TEXT,
        sorted_array TEXT,
        block_size INTEGER
    )''')
    conn.commit()
    conn.close()

# Сохранение массива в БД
def save_array(original_array, sorted_array, block_size):
    conn = sqlite3.connect('arrays.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO arrays (original_array, sorted_array, block_size)
                      VALUES (?, ?, ?)''', (str(original_array), str(sorted_array), block_size))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_type = request.form.get('input_type')
    if input_type == 'manual':
        return process_manual()
    elif input_type == 'random':
        return process_random()
    else:
        return render_template('error.html', message="Invalid input type.")

def process_manual():
    try:
        arr = [float(i) for i in request.form.get('user_input').split()]
        block_size = int(request.form.get('block_size'))
    except ValueError:
        return render_template('error.html', message="Invalid input for manual array.")

    sorted_array = block_sort(arr, block_size)
    save_array(arr, sorted_array, block_size)
    return render_template('result.html', original=arr, sorted=sorted_array, block_size=block_size)

def process_random():
    n = randint(3, 20)  # Генерируем случайное количество элементов
    block_size = randint(1, n)  # Генерируем случайный размер блока
    arr = [round(uniform(-100, 100), 2) for _ in range(n)]  # Генерируем случайные числа
    sorted_array = block_sort(arr, block_size)
    save_array(arr, sorted_array, block_size)
    return render_template('result.html', original=arr, sorted=sorted_array, block_size=block_size)

@app.route('/history')
def history():
    conn = sqlite3.connect('arrays.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM arrays')
    rows = cursor.fetchall()
    conn.close()
    return render_template('history.html', rows=rows)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    conn = sqlite3.connect('arrays.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM arrays')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="arrays"')
    conn.commit()
    conn.close()
    return redirect('/history')

@app.route('/help')
def help_page():
    return render_template('help.html')

# Функция для генерации и добавления случайных массивов
def add_random_arrays(count):
    for _ in range(count):
        n = randint(3, 20)  # Случайный размер массива
        block_size = randint(1, n)  # Случайный размер блока
        arr = [round(uniform(-100, 100), 2) for _ in range(n)]  # Генерация случайного массива
        sorted_array = block_sort(arr, block_size)  # Сортировка массива
        save_array(arr, sorted_array, block_size)  # Сохранение в базу данных

# Тест добавления массивов
def test_add_arrays(count):
    start_time = time.time()
    try:
        add_random_arrays(count)
        elapsed_time = time.time() - start_time
        return {"success": True, "time": elapsed_time}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/test_add_100')
def test_add_100():
    result = test_add_arrays(100)
    return json.dumps(result)

@app.route('/test_add_1000')
def test_add_1000():
    result = test_add_arrays(1000)
    return json.dumps(result)

@app.route('/test_add_10000')
def test_add_10000():
    result = test_add_arrays(10000)
    return json.dumps(result)

# Тест выгрузки и сортировки массивов
def test_sort_arrays(count):
    conn = sqlite3.connect('arrays.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_array, block_size FROM arrays ORDER BY RANDOM() LIMIT ?', (count,))
    arrays = cursor.fetchall()
    conn.close()

    start_time = time.time()
    sorted_times = []
    for row in arrays:
        original_array = eval(row[0])  # Преобразование строки обратно в массив
        block_size = row[1]
        start_sort_time = time.time()
        sorted_array = block_sort(original_array, block_size)  # Сортировка
        elapsed_sort_time = time.time() - start_sort_time
        sorted_times.append(elapsed_sort_time)

    total_time = time.time() - start_time
    avg_time = sum(sorted_times) / len(sorted_times) if sorted_times else 0
    return {"success": True, "total_time": total_time, "average_time": avg_time}

@app.route('/test_sort_100')
def test_sort_100():
    result = test_sort_arrays(100)
    return json.dumps(result)

@app.route('/test_sort_1000')
def test_sort_1000():
    result = test_sort_arrays(1000)
    return json.dumps(result)

@app.route('/test_sort_10000')
def test_sort_10000():
    result = test_sort_arrays(10000)
    return json.dumps(result)

# Тест очистки базы данных
def test_clear_database():
    conn = sqlite3.connect('arrays.db')
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute('DELETE FROM arrays')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="arrays"')
    conn.commit()
    elapsed_time = time.time() - start_time
    conn.close()
    return {"success": True, "time": elapsed_time}

@app.route('/test_clear_100')
def test_clear_100():
    test_add_arrays(100)  # Сначала добавим 100 массивов
    result = test_clear_database()
    return json.dumps(result)

@app.route('/test_clear_1000')
def test_clear_1000():
    test_add_arrays(1000)  # Сначала добавим 1000 массивов
    result = test_clear_database()
    return json.dumps(result)

@app.route('/test_clear_10000')
def test_clear_10000():
    test_add_arrays(10000)  # Сначала добавим 10000 массивов
    result = test_clear_database()
    return json.dumps(result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
