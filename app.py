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
            ('11/11/2025 Mardi', '14h00', None),
            ('11/11/2025 Mardi', '15h15', None),
            ('11/11/2025 Mardi', '16h30', None),
            ('11/11/2025 Mardi', '17h45', None),
            ('11/11/2025 Mardi', '19h00', None),
            ('12/11/2025 Mercredi', '17h15', None),
            ('12/11/2025 Mercredi', '18h30', None),
            ('13/11/2025 Jeudi', '14h00', None),
            ('13/11/2025 Jeudi', '15h15', None),
            ('13/11/2025 Jeudi', '16h30', None),
            ('13/11/2025 Jeudi', '17h45', None),
            ('13/11/2025 Jeudi', '19h00', None),
            ('14/11/2025 Vendredi', '16h15', None),
            ('14/11/2025 Vendredi', '17h30', None),
            ('14/11/2025 Vendredi', '18h45', None),
            ('15/11/2025 Samedi', '09h45', None),
            ('15/11/2025 Samedi', '11h00', None),
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