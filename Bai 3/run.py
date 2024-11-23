from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cần thiết cho việc hiển thị thông báo

# Kết nối cơ sở dữ liệu toàn cục
conn = None
cur = None

# Thông tin kết nối cơ sở dữ liệu (có thể thay đổi trong form)
db_config = {
    "dbname": "dbtest",
    "user": "postgres",
    "password": "12345",
    "host": "localhost",
    "port": "5432"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect_db():
    global conn, cur
    try:
        conn = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        cur = conn.cursor()
        flash("Kết nối cơ sở dữ liệu thành công!", "success")
    except Exception as e:
        flash(f"Lỗi khi kết nối cơ sở dữ liệu: {e}", "error")
    return redirect(url_for('home'))

@app.route('/load_data', methods=['POST'])
def load_data():
    global cur
    table_name = request.form['table_name']
    try:
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cur.execute(query)
        rows = cur.fetchall()
        return render_template('index.html', rows=rows)
    except Exception as e:
        flash(f"Lỗi khi tải dữ liệu: {e}", "error")
        return redirect(url_for('home'))

@app.route('/insert_data', methods=['POST'])
def insert_data():
    global cur
    hovaten = request.form['hovaten']
    diachi = request.form['diachi']
    sosp = int(request.form['sosp'])
    hinhthucthanhtoan = request.form['hinhthucthanhtoan']
    table_name = request.form['table_name']

    try:
        insert_query = sql.SQL("INSERT INTO {} (hovaten, diachi, sosp, hinhthucthanhtoan) VALUES (%s, %s, %s, %s)").format(
            sql.Identifier(table_name)
        )
        cur.execute(insert_query, (hovaten, diachi, sosp, hinhthucthanhtoan))
        conn.commit()
        flash("Dữ liệu đã được chèn thành công!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Lỗi khi chèn dữ liệu: {e}", "error")
    return redirect(url_for('home'))

@app.route('/delete_data', methods=['POST'])
def delete_data():
    global cur
    hovaten = request.form['delete_hovaten']
    table_name = request.form['table_name']

    if not hovaten:
        flash("Vui lòng cung cấp tên để xóa!", "error")
        return redirect(url_for('home'))

    try:
        delete_query = sql.SQL("DELETE FROM {} WHERE hovaten = %s").format(sql.Identifier(table_name))
        cur.execute(delete_query, (hovaten,))
        conn.commit()
        flash("Dữ liệu đã được xóa thành công!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Lỗi khi xóa dữ liệu: {e}", "error")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
