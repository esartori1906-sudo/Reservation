from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "slots.db"

# --- Création de la base de données si elle n'existe pas ---
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE creneaux (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                heure TEXT,
                parent TEXT
            )
        """)
        # Exemples de créneaux (à modifier selon ton planning)
        c.executemany(
            "INSERT INTO creneaux (date, heure, parent) VALUES (?, ?, NULL)",
            [
                ("Lundi", "17h00"),
                ("Mardi", "18h00"),
                ("Mercredi", "17h30"),
                ("Jeudi", "18h30"),
                ("Vendredi", "16h00"),
            ]
        )
        conn.commit()
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# --- Page principale ---
@app.route('/')
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, date AS jour, heure, parent FROM creneaux")
    creneaux = [dict(id=row[0], jour=row[1], heure=row[2], parent=row[3]) for row in c.fetchall()]
    conn.close()
    return render_template('index.html', creneaux=creneaux)

# --- Réserver un créneau ---
@app.route('/reserver/<int:slot_id>', methods=['POST'])
def reserver(slot_id):
    parent = request.form['nom_parent']
    conn = get_db_connection()
    c = conn.cursor()
    # On ne réserve que si le créneau est libre
    c.execute("UPDATE creneaux SET parent=? WHERE id=? AND parent IS NULL", (parent, slot_id))
    conn.commit()
    conn.close()
    return redirect('/')

# --- Page admin pour libérer des créneaux ---
@app.route('/admin')
def admin():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, date AS jour, heure, parent FROM creneaux")
    creneaux = [dict(id=row[0], jour=row[1], heure=row[2], parent=row[3]) for row in c.fetchall()]
    conn.close()
    return render_template('admin.html', creneaux=creneaux)

@app.route('/admin/liberer/<int:slot_id>', methods=['POST'])
def liberer(slot_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE creneaux SET parent=NULL WHERE id=?", (slot_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')


# --- Point d'entrée principal ---
if __name__ == '__main__':
    init_db()
    from os import environ
    # 🔧 Pour Render : écouter sur le port attribué dynamiquement
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)