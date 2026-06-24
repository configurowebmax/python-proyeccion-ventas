"""
=====================================================================
 Proyección de Ventas
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_proyeccion_ventas_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Proyección de Ventas."""

    def __init__(self, ventas_actuales, crecimiento, meses):
        self.ventas_actuales = float(ventas_actuales)
        self.crecimiento = float(crecimiento)
        self.meses = float(meses)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        proyectadas = self.ventas_actuales * ((1 + self.crecimiento / 100) ** self.meses)
        incremento = proyectadas - self.ventas_actuales
        return {"proyectadas": proyectadas, "incremento": incremento}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Proyección con crecimiento compuesto."


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("ventas_actuales"), input_float("crecimiento"), input_float("meses"))
    r = c.calcular()
    html = f"""
      <div class="result-value">🔮 Ventas en {int(c.meses)}m: {fmt_moneda(r["proyectadas"])}</div>
      <p class="result-detail">Incremento: {fmt_moneda(r["incremento"])}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "ventas_actuales": input_float("ventas_actuales"),
            "crecimiento": input_float("crecimiento"),
            "meses": input_float("meses"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
            if "ventas_actuales" in datos:
                document.querySelector("#ventas_actuales").value = datos["ventas_actuales"]
            if "crecimiento" in datos:
                document.querySelector("#crecimiento").value = datos["crecimiento"]
            if "meses" in datos:
                document.querySelector("#meses").value = datos["meses"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
