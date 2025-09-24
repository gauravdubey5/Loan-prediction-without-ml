from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('loan_applications.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loan_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            income INTEGER NOT NULL,
            loan_amount INTEGER NOT NULL,
            credit_score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        income = request.form['income']
        loan_amount = request.form['loan_amount']
        credit_score = request.form['credit_score']
        print(f"Received application: {name}, {age}, {income}, {loan_amount}, {credit_score}")

        conn = sqlite3.connect('loan_applications.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO loan_applications (name, age, income, loan_amount, credit_score) VALUES (?, ?, ?, ?, ?)', 
                       (name, age, income, loan_amount, credit_score))
        conn.commit()
        conn.close()
        return render_template('success.html')
    return render_template('add_application.html')

@app.route('/success')
def success():
    return render_template('success.html')  

@app.route('/applications')
def applications():
    conn = sqlite3.connect('loan_applications.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM loan_applications')
    applications = cursor.fetchall()
    conn.close()
    return render_template('applications.html', applications=applications)

@app.route('/edit/<int:application_id>', methods=['GET', 'POST'])
def edit(application_id):
    conn = sqlite3.connect('loan_applications.db')
    cursor = conn.cursor()
    if request.method=='POST':
        name = request.form['name']
        age = request.form['age']
        income = request.form['income']
        loan_amount = request.form['loan_amount']
        credit_score = request.form['credit_score']
        cursor.execute('UPDATE loan_applications SET name=?, age=?, income=?,loan_amount=?, credit_score=? WHERE id=?', (name, age, income, loan_amount, credit_score, application_id))
        conn.commit()
        conn.close()
        return render_template('applications.html')
    else:
        cursor.execute('SELECT * FROM loan_applications WHERE id=?', (application_id,))
        application = cursor.fetchone()
        conn.close()
        return render_template('edit.html', application=application)

@app.route('/delete/<int:application_id>', methods=['GET', 'POST'])
def delete(application_id):
    conn = sqlite3.connect('loan_applications.db')
    cursor =conn.cursor()
    cursor.execute('DELETE  FROM loan_applications WHERE id=?',(application_id,))
    conn.commit()
    conn.close()
    return redirect (url_for('applications'))



if __name__ == '__main__':
    init_db()
    app.run(debug=True)