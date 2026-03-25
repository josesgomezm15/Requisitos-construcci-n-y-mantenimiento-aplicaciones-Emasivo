from flask import Flask, render_template, request, redirect, url_for, session, flash
import re
from db import get_connection

app = Flask(__name__)
app.secret_key = "clave-secreta-segura-cambiar-en-produccion"


def validar_credencial(valor: str) -> tuple[bool, str]:
    if len(valor) < 8:
        return False, "Debe tener al menos 8 caracteres."
    if not re.fullmatch(r"[A-Za-z0-9]+", valor):
        return False, "Solo se permiten letras y números."
    return True, ""


@app.route("/", methods=["GET", "POST"])
def login():
    if "usuario" in session:
        return redirect(url_for("dashboard"))

    error_usuario = ""
    error_password = ""
    usuario_ingresado = ""

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()
        usuario_ingresado = usuario

        valido_u, msg_u = validar_credencial(usuario)
        if not valido_u:
            error_usuario = f"Usuario inválido: {msg_u}"

        valido_p, msg_p = validar_credencial(password)
        if not valido_p:
            error_password = f"Contraseña inválida: {msg_p}"

        
        if valido_u and valido_p:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT username, password FROM usuarios WHERE username = ?",
                (usuario,)
            )

            user = cursor.fetchone()
            conn.close()

            if user and user.password == password:
                session["usuario"] = usuario
                return redirect(url_for("dashboard"))
            else:
                error_usuario = "Usuario o contraseña incorrectos."

    return render_template(
        "login.html",
        error_usuario=error_usuario,
        error_password=error_password,
        usuario_ingresado=usuario_ingresado,
    )


@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", usuario=session["usuario"])


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)