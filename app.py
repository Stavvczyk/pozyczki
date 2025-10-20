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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM szybkie_dodawanie;")
    szybkie_lista = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('dodaj.html', szybkie_lista=szybkie_lista)

@app.route('/dodaj', methods=['post'])
def dodaj():
    osoba = request.form.get('osoba')
    kwota = request.form.get('kwota')
    opis = request.form.get('opis')
    typ = request.form.get('typ')
    data = request.form.get('data')
    anulowane = request.form.get('anulowany')

    if anulowane == "Anuluj":
        return redirect('/')

    if not data:
        from datetime import date
        data = str(date.today())

    if not osoba:
        return render_template('dodaj.html', error="Nie podano osoby", osoba=osoba, kwota=kwota, opis=opis)
    if not kwota:
        return render_template('dodaj.html', error="Nie podano kwoty", osoba=osoba, kwota=kwota, opis=opis)
    if not opis:
        return render_template('dodaj.html', error="Nie podano opisu", osoba=osoba, kwota=kwota, opis=opis)
    
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

@app.route('/dodaj-szybkie-dodawanie')
def szybkie_dodawanie_tworzenie():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM szybkie_dodawanie;")
    szybkie_lista = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('szybkie_dodawanie.html', szybkie_lista=szybkie_lista)

@app.route('/szybkie-dodawanie', methods=['post'])
def szybkie_dodawanie_dodaj_do_bazy():
    osoba = request.form.get('osoba')
    kwota = request.form.get('kwota')
    opis = request.form.get('opis')
    typ = request.form.get('typ')
    data = request.form.get('data')
    skrot = request.form.get('skrot')
    anulowane = request.form.get('anulowany')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM szybkie_dodawanie;")
    szybkie_lista = cursor.fetchall()

    if anulowane == "Powrót":
        return redirect('/dodaj')

    if not data:
        from datetime import date
        data = str(date.today())

    if not osoba:
        return render_template('szybkie_dodawanie.html',
                                error="Nie podano osoby",
                                szybkie_lista=szybkie_lista,
                                osoba=osoba,
                                kwota=kwota,
                                opis=opis,
                                skrot=skrot)
    if not kwota:
        return render_template('szybkie_dodawanie.html', 
                               error="Nie podano kwoty", 
                               szybkie_lista=szybkie_lista,
                               osoba=osoba,
                               kwota=kwota,
                               opis=opis,
                               skrot=skrot)
    if not opis:
        return render_template('szybkie_dodawanie.html', 
                               error="Nie podano opisu", 
                               szybkie_lista=szybkie_lista,
                               osoba=osoba,
                               kwota=kwota,
                               opis=opis,
                               skrot=skrot)
    if not skrot:
        return render_template('szybkie_dodawanie.html', 
                               error="Nie podano nazwy akcji", 
                               szybkie_lista=szybkie_lista,
                               osoba=osoba,
                               kwota=kwota,
                               opis=opis,
                               skrot=skrot)
    
    
    cursor.execute("INSERT INTO szybkie_dodawanie (osoba, kwota, opis, typ, data, skrot) VALUES (%s, %s, %s, %s, %s, %s)", (osoba, kwota, opis, typ, data, skrot))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('/')

@app.route('/usuwanie-szybkich-akcji', methods=['post'])
def usuwanie_szybkich_akcji():
    lista_do_usuniecia = request.form.getlist('szybkie_do_usuniecia')
    conn = get_db_connection()
    cursor = conn.cursor()
    for id in lista_do_usuniecia:
        cursor.execute("DELETE FROM szybkie_dodawanie WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.commit()
    return redirect('/dodaj-szybkie-dodawanie')

@app.route('/szybki-wpis', methods=['post'])
def dodaj_szybki_wpis():
    skrot = request.form.get('skrot')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM szybkie_dodawanie WHERE skrot = %s", (skrot,))
    conn.commit()

    dane_do_dodania = cursor.fetchone()#jeśli się jedno dodaje a 2 nie to najprawdopodobniej skrot jest taki sam choć nie powinien
    osoba = dane_do_dodania[1]
    kwota = dane_do_dodania[2]
    opis = dane_do_dodania[3]
    typ = dane_do_dodania[4]
    from datetime import date
    data = str(date.today())
    cursor.execute("INSERT INTO pozyczki (osoba, kwota, opis, typ, data) VALUES (%s, %s, %s, %s, %s)", (osoba, kwota, opis, typ, data))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

if __name__=='__main__':
    app.run(debug = True)