from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
USERS_FILE = 'users.json'

#def load_users():
   # try:
       #if not os.path.exists(USERS_FILE):
           # return {}
        #with open(USERS_FILE, 'r') as f:
            #return json.load(f)
    #except (json.JSONDecodeError, IOError) as e:
       # print(f"Error loading users: {e}")
        #return {}

#def save_users(users):
    
   # try:
        #ith open(USERS_FILE, 'w') as f:
           # json.dump(users, f, indent=4)
    #except IOError as e:
       # print(f"Error saving users: {e}")

@app.route('/')
def zacetna():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def prijava():
    if request.method == 'POST':
        uporabnisko_ime = request.form.get('uporabnisko_ime')
        geslo = request.form.get('geslo')

        uporabniki = nalozi_uporabnike()

        if uporabnisko_ime in uporabniki and uporabniki[uporabnisko_ime]['geslo'] == geslo:
            session['uporabnisko_ime'] = uporabnisko_ime
            return redirect(url_for('menu'))
        else:
            return render_template('login.html', napaka="Neveljavni podatki")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def registracija():
    if request.method == 'POST':
        uporabnisko_ime = request.form.get('uporabnisko_ime')
        e_posta = request.form.get('e_posta')
        geslo = request.form.get('geslo')
        potrdi_geslo = request.form.get('potrdi_geslo')

        if not all([uporabnisko_ime, e_posta, geslo, potrdi_geslo]):
            return render_template('register.html', napaka="Vsa polja so obvezna")

        if geslo != potrdi_geslo:
            return render_template('register.html', napaka="Gesli se ne ujemata")

        uporabniki = nalozi_uporabnike()

        if uporabnisko_ime in uporabniki:
            return render_template('register.html', napaka="Uporabniško ime že obstaja")

        uporabniki[uporabnisko_ime] = {
            'e_posta': e_posta,
            'geslo': geslo  
        }

        shrani_uporabnike(uporabniki)
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/menu')
def meni():
    if 'uporabnisko_ime' not in session:
        return redirect(url_for('prijava'))
    return render_template('menu.html', uporabnisko_ime=session['uporabnisko_ime'])


@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/lawyer/<specialty>')
def lawyer_chat(specialty):
    """Route for lawyer-specific chat."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('lawyer_chat.html', specialty=specialty)


if __name__ == '__main__':
    app.run(debug=True)