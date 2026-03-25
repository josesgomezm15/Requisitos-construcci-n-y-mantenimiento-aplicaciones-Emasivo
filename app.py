from flask import Flask, render_template, request, redirect, url_for, session
import re
from db import get_connection

app = Flask(__name__)
app.secret_key = "clave-secreta-segura-cambiar-en-produccion"


# 🔐 VALIDACIÓN
def validar_credencial(valor: str) -> tuple[bool, str]:
    if len(valor) < 10:
        return False, "Debe tener al menos 10 caracteres."
    if not re.fullmatch(r"[A-Za-z0-9]+", valor):
        return False, "Solo se permiten letras y números."
    return True, ""


# 🔑 LOGIN
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

        # Validaciones
        valido_u, msg_u = validar_credencial(usuario)
        if not valido_u:
            error_usuario = f"Usuario inválido: {msg_u}"

        valido_p, msg_p = validar_credencial(password)
        if not valido_p:
            error_password = f"Contraseña inválida: {msg_p}"

        # Si todo está válido → BD
        if valido_u and valido_p:
            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT username, password FROM usuarios WHERE username = ?",
                    (usuario,)
                )

                user = cursor.fetchone()

                if user:
                    db_password = user[1].strip()

                    if db_password == password:
                        session["usuario"] = usuario
                        return redirect(url_for("dashboard"))
                    else:
                        error_usuario = "Contraseña incorrecta."
                else:
                    error_usuario = "Usuario no existe."

                conn.close()

            except Exception as e:
                error_usuario = "Error de conexión con la base de datos"
                print("ERROR LOGIN:", e)

    return render_template(
        "login.html",
        error_usuario=error_usuario,
        error_password=error_password,
        usuario_ingresado=usuario_ingresado,
    )


# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", usuario=session["usuario"])


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# 🔐 CAMBIAR CONTRASEÑA
@app.route("/cambiar_password", methods=["GET", "POST"])
def cambiar_password():
    if "usuario" not in session:
        return redirect(url_for("login"))

    mensaje = ""

    if request.method == "POST":
        actual = request.form.get("actual", "").strip()
        nueva = request.form.get("nueva", "").strip()

        # Validar nueva contraseña
        valido, msg = validar_credencial(nueva)
        if not valido:
            return render_template("cambiar_password.html", mensaje=msg)

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT password FROM usuarios WHERE username = ?",
                (session["usuario"],)
            )

            user = cursor.fetchone()

            if user:
                db_password = user[0].strip()

                if db_password == actual:
                    cursor.execute(
                        "UPDATE usuarios SET password = ? WHERE username = ?",
                        (nueva, session["usuario"])
                    )
                    conn.commit()
                    mensaje = "✅ Contraseña actualizada correctamente"
                else:
                    mensaje = "❌ Contraseña actual incorrecta"
            else:
                mensaje = "❌ Usuario no encontrado"

            conn.close()

        except Exception as e:
            mensaje = "❌ Error al actualizar contraseña"
            print("ERROR PASSWORD:", e)

    return render_template("cambiar_password.html", mensaje=mensaje)


# ▶️ EJECUCIÓN
if __name__ == "__main__":
    app.run(debug=True)