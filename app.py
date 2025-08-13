from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), 'budget.db')

def init_db():
    con = sqlite3.connect(DB)
    con.execute('CREATE TABLE IF NOT EXISTS txns (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, amount REAL, note TEXT)')
    con.commit(); con.close()

@app.route('/', methods=['GET'])
def index():
    con = sqlite3.connect(DB)
    rows = con.execute('SELECT id,date,category,amount,note FROM txns ORDER BY date DESC, id DESC').fetchall()
    total = con.execute('SELECT IFNULL(SUM(amount),0) FROM txns').fetchone()[0]
    con.close()
    return render_template('index.html', rows=rows, total=total)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    note = request.form.get('note','')
    con = sqlite3.connect(DB)
    con.execute('INSERT INTO txns (date,category,amount,note) VALUES (?,?,?,?)', (date,category,amount,note))
    con.commit(); con.close()
    return redirect('/')

@app.route('/delete/<int:tid>')
def delete(tid):
    con = sqlite3.connect(DB)
    con.execute('DELETE FROM txns WHERE id=?', (tid,))
    con.commit(); con.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
