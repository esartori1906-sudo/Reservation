from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def init_db():
    print("🔧 Initialisation de la base de données...")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS creneaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            heure TEXT NOT NULL,
            parent TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Base initialisée ou déjà existante.")

# Appel au démarrage
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, date AS jour, heure, parent FROM creneaux")
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/add", methods=["POST"])
def add_creneau():
    data = request.get_json()
    date = data.get("date")
    heure = data.get("heure")
    parent = data.get("parent")

    if not date or not heure:
        return jsonify({"error": "date et heure sont obligatoires"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO creneaux (date, heure, parent) VALUES (?, ?, ?)", (date, heure, parent))
    conn.commit()
    conn.close()

    return jsonify({"message": "Créneau ajouté avec succès"}), 201

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_creneau(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM creneaux WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Créneau {id} supprimé"}), 200

# ✅ Route spéciale pour initialiser manuellement la base
@app.route("/init")
def force_init():
    init_db()
    return jsonify({"message": "Base (re)créée avec succès"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)