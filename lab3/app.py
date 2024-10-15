import sqlite3
from random import *

from flask import Flask, request, render_template, redirect

from __init__ import *

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
    print("Input Type: ", input_type)  # Проверка типа ввода
    arr = []
    block_size = 0
    sorted_array = []

    if input_type == 'manual':
        arr = [float(i) for i in request.form.get('user_input').split()]
        block_size = int(request.form.get('block_size'))
    elif input_type == 'random':
        n = randint(3, 20)
        block_size = randint(1, n)
        arr = [uniform(-100, 100) for _ in range(n)]
        arr = [round(num, 2) for num in arr]

    print("Generated Array: ", arr)  # Проверка сгенерированного массива

    sorted_array = block_sort(arr, block_size)

    print("Sorted Array: ", sorted_array)  # Проверка отсортированного массива

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
    conn.commit()
    conn.close()
    return redirect('/history')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
