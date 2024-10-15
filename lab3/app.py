import sqlite3
from random import randint, uniform
from flask import Flask, request, render_template, redirect
from __init__ import block_sort  # Импортируем функцию сортировки

# Настройка приложения Flask
app = Flask(__name__)


# Создание базы данных и таблицы
def init_db():
    conn = sqlite3.connect('arrays.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arrays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_array TEXT,
            sorted_array TEXT,
            block_size INTEGER
        )
    ''')
    conn.commit()
    conn.close()


# Сохранение массива в БД
def save_array(original_array, sorted_array, block_size):
    conn = sqlite3.connect('arrays.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO arrays (original_array, sorted_array, block_size)
        VALUES (?, ?, ?)
    ''', (str(original_array), str(sorted_array), block_size))
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

    print("Manual Input Array:", arr)
    print("Block Size:", block_size)
    print("Sorted Array:", sorted_array)

    save_array(arr, sorted_array, block_size)

    return render_template('result.html', original=arr, sorted=sorted_array, block_size=block_size)

def process_random():
    n = randint(3, 20)  # Генерируем случайное количество элементов
    block_size = randint(1, n)  # Генерируем случайный размер блока
    arr = [round(uniform(-100, 100), 2) for _ in range(n)]  # Генерируем случайные числа

    sorted_array = block_sort(arr, block_size)

    print("Generated Random Array:", arr)
    print("Block Size:", block_size)
    print("Sorted Array:", sorted_array)

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
    # Сбросить счётчик ID
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="arrays"')
    conn.commit()
    conn.close()
    return redirect('/history')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
