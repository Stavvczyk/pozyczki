from flask import Flask, redirect, request, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
    host="dpg-d3pa50hr0fns73afnrd0-a.frankfurt-postgres.render.com",
    database="pozyczki_db",
    user="pozyczki_db_user",
    password="3Ez2JQS6c1GJVunGJ5dz0tcCpp9P0SvY",
    port="5432"
)
    return conn
    
pozyczki = []

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pozyczki;")
    pozyczki = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', pozyczki=pozyczki)

@app.route('/dodaj')
def dodaj_wyswietlnie():
    return render_template('dodaj.html')

@app.route('/dodaj', methods=['post'])
def dodaj():
    osoba = request.form.get('osoba')
    kwota = request.form.get('kwota')
    opis = request.form.get('opis')
    typ = request.form.get('typ')
    data = request.form.get('data')

    if not data:
        from datetime import date
        data = str(date.today())

    if not osoba:
        return render_template('dodaj.html', error="Nie podano osoby") # na tej podstawie możesz dodać później uzupełnianie
    if not kwota:
        return render_template('dodaj.html', error="Nie podano kwoty")
    if not opis:
        return render_template('dodaj.html', error="Nie podano opisu")
    # jeśli by dać że jeśli coś jest to przekazać to i w html dać w okienkach textowych value że to to co przekazane

    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pozyczki (osoba, kwota, opis, typ, data) VALUES (%s, %s, %s, %s, %s)", (osoba, kwota, opis, typ, data))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('/')

@app.route('/usun-zaznaczone', methods=['post'])
def usun_zaznaczone():
    do_usuniecia = request.form.getlist('usun-zaznaczone')
    conn = get_db_connection()
    cursor = conn.cursor()
    for id in do_usuniecia:
        cursor.execute("DELETE FROM pozyczki WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('/')

if __name__=='__main__':
    app.run(debug = True)