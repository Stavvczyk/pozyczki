from flask import Flask, redirect, request, render_template

app = Flask(__name__)

pozyczki = []

@app.route('/')
def home():
    return render_template('index.html', pozyczki=pozyczki)

@app.route('/dodaj')
def dodaj_wyswietlnie():
    return render_template('dodaj.html')

@app.route('/dodaj', methods=['post'])
def dodaj():
    osoba = request.form.get('osoba')
    kwota = request.form.get('kwota')
    typ = request.form.get('typ')
    data = request.form.get('data')

    if not data:
        from datetime import date
        data = str(date.today())

    if not osoba:
        return render_template('dodaj.html', error="Nie podano osoby")
    if not kwota:
        return render_template('dodaj.html', error="Nie podano kwoty")
    
    pozyczki.append({
        "osoba" : osoba,
        "kwota" : kwota,
        "typ" : typ,
        "data" : data
    })
    
    return redirect('/')

@app.route('/usun-zaznaczone', methods=['post'])
def usun_zaznaczone():
    if pozyczki:
        do_usuniecia = request.form.getlist('usun-zaznaczone')
        if do_usuniecia:
            do_usuniecia = sorted(map(int, do_usuniecia), reverse=True)
            for usun in do_usuniecia:
                pozyczki.pop(usun)
    return redirect('/')

if __name__=='__main__':
    app.run(debug = True)