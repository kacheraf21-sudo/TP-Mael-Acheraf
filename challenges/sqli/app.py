from flask import Flask, request, g
import sqlite3, os

app = Flask(__name__)
DB = 'sqli.db'

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = sqlite3.connect(DB)
    return db

@app.teardown_appcontext
def close_db(exc):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    q = request.args.get('user', '')
    # vulnérable : concaténation directe -> SQLi
    cur = get_db().cursor()
    sql = "SELECT message FROM messages WHERE user = '%s';" % q
    cur.execute(sql)
    rows = cur.fetchall()
    return '<br>'.join([r[0] for r in rows]) or "No messages"

if __name__ == '__main__':
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("CREATE TABLE messages(user TEXT, message TEXT);")
        c.execute("CREATE TABLE flags(name TEXT, value TEXT);")
        c.execute("INSERT INTO messages VALUES ('alice','hello');")
        c.execute("INSERT INTO flags VALUES ('sqli','FLAG{sql_injection_success}');")
        conn.commit()
        conn.close()
    app.run(host='0.0.0.0', port=5001)
