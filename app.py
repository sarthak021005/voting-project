
from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "project2026"

def getConnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",   # CHANGE THIS TO YOUR MYSQL PASSWORD
        database="evm"
    )

# -------- WELCOME PAGE --------
@app.route('/')
def welcome():
    return render_template("welcome.html")

# -------- OPEN REGISTER PAGE --------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        address = request.form.get('address')

        if not name or not email or not password:
            flash("Name, Email and Password are required")
            return redirect('/register')

        con = getConnection()
        cur = con.cursor()
        cur.execute("INSERT INTO voter(name,email,password,age,address) VALUES(%s,%s,%s,%s,%s)",
                    (name,email,password,age,address))
        con.commit()

        flash("Registration Successful - Please Login")
        return redirect('/login/voter')

    return render_template("register.html")

# -------- LOGIN PAGE --------
@app.route('/login/<type>')
def login(type):
    return render_template("login.html", type=type)

# -------- VOTER LOGIN --------
@app.route('/voter_login', methods=['POST'])
def voter_login():
    email = request.form['email']
    password = request.form['password']

    con = getConnection()
    cur = con.cursor()
    cur.execute("SELECT voter_id,voted FROM voter WHERE email=%s AND password=%s",
                (email,password))
    d = cur.fetchone()

    if d:
        session['voter'] = d[0]
        session['voted'] = d[1]
        return redirect('/dashboard')

    flash("Invalid Login")
    return redirect('/login/voter')

# -------- ADMIN LOGIN --------
@app.route('/admin_login', methods=['POST'])
def admin_login():
    u = request.form['email']
    p = request.form['password']

    con = getConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s",(u,p))

    if cur.fetchone():
        session['admin'] = True
        return redirect('/dashboard')

    flash("Invalid Admin Login")
    return redirect('/login/admin')

# -------- DASHBOARD --------
@app.route('/dashboard')
def dashboard():
    con = getConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM candidate")
    c = cur.fetchall()

    if 'admin' in session:
        return render_template("admin.html", candidates=c)

    if 'voter' in session:
        return render_template("vote.html", candidates=c, voted=session['voted'])

    return redirect('/')

# -------- ADD CANDIDATE --------
@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    name = request.form['name']
    party = request.form['party']

    con = getConnection()
    cur = con.cursor()
    cur.execute("INSERT INTO candidate(name,party,election_id) VALUES(%s,%s,1)",
                (name,party))
    con.commit()

    flash("Candidate Added")
    return redirect('/dashboard')

# -------- CAST VOTE --------
@app.route('/cast', methods=['POST'])
def cast():
    if session.get('voted') == 1:
        flash("You already voted")
        return redirect('/dashboard')

    cid = request.form['cid']
    vid = session['voter']

    con = getConnection()
    cur = con.cursor()

    cur.execute("INSERT INTO vote(voter_id,candidate_id,election_id) VALUES(%s,%s,1)",
                (vid,cid))

    cur.execute("UPDATE voter SET voted=1 WHERE voter_id=%s",(vid,))
    con.commit()

    session['voted'] = 1
    flash("Vote Cast Successfully")
    return redirect('/dashboard')

# -------- RESULT --------
@app.route('/result')
def result():
    con = getConnection()
    cur = con.cursor()
    cur.execute("""
        SELECT candidate.name, COUNT(vote.vote_id)
        FROM candidate LEFT JOIN vote
        ON candidate.candidate_id = vote.candidate_id
        GROUP BY candidate.name
    """)
    r = cur.fetchall()
    return render_template("result.html", r=r)

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
