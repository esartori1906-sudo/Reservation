from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Initialisation de la base ---
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS creneaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            heure TEXT NOT NULL,
            parent TEXT
        )
    ''')
    # Créneaux par défaut
    c.execute("SELECT COUNT(*) FROM creneaux")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO creneaux (date, heure, parent) VALUES (?, ?, ?)", [
            ('02/12/2025 Mardi', '18h15', None),
            ('04/12/2025 Jeudi', '09h30', None),
            ('04/12/2025 Jeudi', '10h45', None),
            ('05/12/2025 Vendredi', '17h15', None),
            ('05/12/2025 Vendredi', '18h30', None),
            ('06/12/2025 Samedi', '09h45', None),
            ('06/12/2025 Samedi', '11h00', None),
            ('06/12/2025 Samedi', '14h00', None),
            ('06/12/2025 Samedi', '15h15', None),
            ('06/12/2025 Samedi', '16h30', None),
            ('06/12/2025 Samedi', '17h45', None),
        ])
    conn.commit()
    conn.close()

init_db()

# --- Page principale ---
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, date, heure, parent FROM creneaux ORDER BY date, heure")
    creneaux = c.fetchall()
    conn.close()
    return render_template('index.html', creneaux=creneaux)

# --- Réservation d’un créneau ---
@app.route('/reserver/<int:id>', methods=['POST'])
def reserver(id):
    nom_enfant = request.form['nom_enfant']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE creneaux SET parent = ? WHERE id = ?", (nom_enfant, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)