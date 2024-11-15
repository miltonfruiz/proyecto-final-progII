from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    payment_option TEXT,
                    payment_method TEXT,
                    card_type TEXT)''')
    c.execute("PRAGMA table_info(subscribers);")
    columns = [column[1] for column in c.fetchall()]
    if 'phone' not in columns:
        c.execute('ALTER TABLE subscribers ADD COLUMN phone TEXT')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, phone, payment_option, payment_method, card_type FROM subscribers")
    subscribers = [
        {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'phone': row[3],
            'payment_option': row[4],
            'payment_method': row[5],
            'card_type': row[6]
        } for row in c.fetchall()
    ]
    conn.close()
    return render_template('index.html', subscribers=subscribers)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    payment_option = data['paymentOption']
    payment_method = data['paymentMethod']
    card_type = data.get('cardType', '')


    if not name or not email or not payment_option or not payment_method:
        return jsonify(success=False, message="Faltan datos requeridos")

    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute("INSERT INTO subscribers (name, email, phone, payment_option, payment_method, card_type) VALUES (?, ?, ?, ?, ?, ?)",
              (name, email, phone, payment_option, payment_method, card_type))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@app.route('/get_subscribers', methods=['GET'])
def get_subscribers():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, phone, payment_option, payment_method, card_type FROM subscribers")
    subscribers = [
        {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'phone': row[3],
            'payment_option': row[4],
            'payment_method': row[5],
            'card_type': row[6]
        } for row in c.fetchall()
    ]
    conn.close()
    return jsonify(subscribers)

@app.route('/edit_subscriber/<int:id>', methods=['POST'])
def edit_subscriber(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    payment_option = data.get('paymentOption')
    payment_method = data.get('paymentMethod')
    card_type = data.get('cardType', '')
    if not name or not email or not payment_option or not payment_method:
        return jsonify(success=False, message="Faltan datos requeridos")

    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('''UPDATE subscribers
                 SET name = ?, email = ?, phone = ?, payment_option = ?, payment_method = ?, card_type = ?
                 WHERE id = ?''',
              (name, email, phone, payment_option, payment_method, card_type, id))
    conn.commit()
    conn.close()

    return jsonify(success=True)

@app.route('/delete_subscriber/<int:id>', methods=['DELETE'])
def delete_subscriber(id):
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('DELETE FROM subscribers WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify(success=True)

@app.route('/internacional')
def internacional():
    return render_template('delfi-internacional.html')

@app.route('/redirect_to_index')
def redirect_to_index():
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
