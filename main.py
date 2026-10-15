from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
# Kunci ini wajib ada buat nyimpen sesi login (biar web inget siapa yang lagi login)
app.secret_key = "ahlele ahlelah" 

# Database sederhana
users = {
    "apiu": "12345",
}

# 1. HALAMAN LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    pesan_error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Cek apakah username dan password cocok
        if username in users and users[username] == password:
            session["user_saat_ini"] = username  # Simpan status login
            return redirect(url_for("home"))     # Lempar ke halaman home
        else:
            pesan_error = "Username atau password salah!"

    # Ini tampilan kotak login web-nya (menggunakan HTML)
    html = """
    <div style="text-align: center; margin-top: 50px; font-family: Arial;">
        <h2>Sistem Login Web</h2>
        <p style="color: red;">{{ pesan_error }}</p>
        <form method="POST">
            <input type="text" name="username" placeholder="Masukkan Username" required><br><br>
            <input type="password" name="password" placeholder="Masukkan Password" required><br><br>
            <button type="submit">Masuk</button>
        </form>
    </div>
    """
    return render_template_string(html, pesan_error=pesan_error)

# 2. HALAMAN HOME (Setelah berhasil login)
@app.route("/home")
def home():
    # Cek apakah user udah login belum
    if "user_saat_ini" in session:
        user = session["user_saat_ini"]
        html = f"""
        <div style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h2 style="color: green;">Login Berhasil!</h2>
            <p>Selamat datang di website, <b>{user}</b>.</p>
            <a href="/logout"><button>Logout</button></a>
        </div>
        """
        return html
    
    # Kalau belum login tapi maksa masuk ke /home, lempar balik ke halaman login
    return redirect(url_for("login"))

# 3. FITUR LOGOUT
@app.route("/logout")
def logout():
    session.pop("user_saat_ini", None) # Hapus sesi login
    return redirect(url_for("login"))  # Balikin ke halaman depan

# Jalanin server web-nya
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
