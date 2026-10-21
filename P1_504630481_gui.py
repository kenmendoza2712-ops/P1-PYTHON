"""
Proyecto 1 - BIS08 Estructuras de Datos
Interfaz gráfica (Tkinter) para el Caso 2: turnos de ventanilla en rondas
(lista circular simple).

Esta interfaz NO modifica la estructura: solo importa y usa la clase
ColaTurnosCircular tal como está.

Cómo ejecutar (en la misma carpeta que P1_<carnet>_estructura.py):
    python P1_<carnet>_gui.py
"""
import glob
import importlib.util
import math
import os
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

# ---------------------------------------------------------------------------
# Carga de la estructura (igual que en el demo)
# ---------------------------------------------------------------------------
carpeta = os.path.dirname(os.path.abspath(__file__))
ruta = glob.glob(os.path.join(carpeta, "P1_*_estructura.py"))[0]
spec = importlib.util.spec_from_file_location("estructura", ruta)
estructura = importlib.util.module_from_spec(spec)
spec.loader.exec_module(estructura)
ColaTurnosCircular = estructura.ColaTurnosCircular

# ---------------------------------------------------------------------------
# Paleta azules / verdes
# ---------------------------------------------------------------------------
AZUL_OSCURO = "#0B3C5D"
AZUL = "#1D70A2"
AZUL_CLARO = "#D6EAF8"
VERDE = "#2E9E7B"
VERDE_OSCURO = "#1F7A5C"
VERDE_CLARO = "#D5F5E3"
FONDO = "#F2F8FB"
BLANCO = "#FFFFFF"
TEXTO = "#12304A"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Turnos de ventanilla - Lista circular")
        self.geometry("920x560")
        self.minsize(820, 500)
        self.configure(bg=FONDO)

        self.cola = ColaTurnosCircular()

        self._estilos()
        self._construir()
        self.refrescar()

    # ------------------------------------------------------------------ UI
    def _estilos(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background=FONDO)
        s.configure("Panel.TFrame", background=BLANCO)
        s.configure("TLabel", background=BLANCO, foreground=TEXTO,
                    font=("Segoe UI", 10))
        s.configure("Azul.TButton", background=AZUL, foreground=BLANCO,
                    font=("Segoe UI", 10, "bold"), padding=7, borderwidth=0)
        s.map("Azul.TButton", background=[("active", AZUL_OSCURO)])
        s.configure("Verde.TButton", background=VERDE, foreground=BLANCO,
                    font=("Segoe UI", 10, "bold"), padding=7, borderwidth=0)
        s.map("Verde.TButton", background=[("active", VERDE_OSCURO)])
        s.configure("TEntry", padding=5)

    def _construir(self):
        # Encabezado
        enc = tk.Frame(self, bg=AZUL_OSCURO, height=60)
        enc.pack(fill="x")
        tk.Label(enc, text="Turnos de ventanilla por rondas",
                 bg=AZUL_OSCURO, fg=BLANCO,
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=20, pady=14)
        tk.Label(enc, text="Lista circular simple", bg=AZUL_OSCURO,
                 fg=VERDE_CLARO, font=("Segoe UI", 10)).pack(side="right", padx=20)

        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill="both", expand=True, padx=14, pady=14)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        # ----- Panel izquierdo: controles
        izq = ttk.Frame(cuerpo, style="Panel.TFrame", padding=14)
        izq.grid(row=0, column=0, sticky="ns", padx=(0, 12))

        ttk.Label(izq, text="Nombre del cliente",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.var_nombre = tk.StringVar()
        entrada = ttk.Entry(izq, textvariable=self.var_nombre, width=26)
        entrada.pack(fill="x", pady=(4, 10))
        entrada.bind("<Return>", lambda e: self.insertar())
        entrada.focus()

        ttk.Button(izq, text="Insertar al final", style="Azul.TButton",
                   command=self.insertar).pack(fill="x", pady=3)
        ttk.Button(izq, text="Buscar", style="Azul.TButton",
                   command=self.buscar).pack(fill="x", pady=3)
        ttk.Button(izq, text="Eliminar", style="Azul.TButton",
                   command=self.eliminar).pack(fill="x", pady=3)

        ttk.Separator(izq).pack(fill="x", pady=12)

        ttk.Button(izq, text="Atender y avanzar", style="Verde.TButton",
                   command=self.atender).pack(fill="x", pady=3)

        ttk.Separator(izq).pack(fill="x", pady=12)

        # Indicadores
        self.lbl_turno = tk.Label(izq, text="", bg=VERDE_CLARO, fg=VERDE_OSCURO,
                                  font=("Segoe UI", 11, "bold"), pady=8,
                                  wraplength=210)
        self.lbl_turno.pack(fill="x", pady=3)
        self.lbl_ronda = tk.Label(izq, text="", bg=AZUL_CLARO, fg=AZUL_OSCURO,
                                  font=("Segoe UI", 10, "bold"), pady=6)
        self.lbl_ronda.pack(fill="x", pady=3)
        self.lbl_total = tk.Label(izq, text="", bg=AZUL_CLARO, fg=AZUL_OSCURO,
                                  font=("Segoe UI", 10, "bold"), pady=6)
        self.lbl_total.pack(fill="x", pady=3)

        # ----- Panel derecho: dibujo + mensajes
        der = ttk.Frame(cuerpo, style="Panel.TFrame", padding=10)
        der.grid(row=0, column=1, sticky="nsew")
        der.rowconfigure(0, weight=1)
        der.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(der, bg=BLANCO, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda e: self.dibujar())

        self.var_msg = tk.StringVar(value="Listo. Inserte clientes para comenzar.")
        tk.Label(der, textvariable=self.var_msg, bg=AZUL_CLARO, fg=AZUL_OSCURO,
                 font=("Segoe UI", 10), anchor="w", padx=10, pady=8,
                 wraplength=560, justify="left").grid(row=1, column=0,
                                                      sticky="ew", pady=(8, 0))

    # ------------------------------------------------------------ acciones
    def _nombre(self):
        return self.var_nombre.get().strip()

    def _mensaje(self, texto):
        self.var_msg.set(texto)

    def insertar(self):
        nombre = self._nombre()
        if not nombre:
            self._mensaje("Escriba un nombre para insertar.")
            return
        self.cola.insertar_final(nombre)
        self.var_nombre.set("")
        self._mensaje(f"Se insertó a {nombre} al final de la ronda.")
        self.refrescar()

    def atender(self):
        atendido = self.cola.atender_y_avanzar()
        if atendido is None:
            self._mensaje("No hay clientes en la cola.")
        else:
            self._mensaje(f"Atendido: {atendido}. "
                          f"Turno siguiente: {self.cola.turno_actual()}.")
        self.refrescar()

    def buscar(self):
        nombre = self._nombre()
        if not nombre:
            self._mensaje("Escriba un nombre para buscar.")
            return
        r = self.cola.buscar(nombre)
        if r is None or r is False:
            self._mensaje(f"{nombre} no está en la cola.")
        else:
            self._mensaje(f"{nombre} sí está en la cola.")

    def eliminar(self):
        nombre = self._nombre()
        if not nombre:
            self._mensaje("Escriba un nombre para eliminar.")
            return
        r = self.cola.eliminar(nombre)
        if r is None or r is False:
            self._mensaje(f"No se pudo eliminar: {nombre} no está en la cola.")
        else:
            self._mensaje(f"Se eliminó a {nombre}.")
            self.var_nombre.set("")
        self.refrescar()

    # ------------------------------------------------------------- vista
    def refrescar(self):
        actual = self.cola.turno_actual()
        self.lbl_turno.config(
            text=f"Turno actual:\n{actual}" if actual is not None
            else "Turno actual:\n—")
        self.lbl_ronda.config(text=f"Ronda en curso: {self.cola.ronda}")
        self.lbl_total.config(text=f"Clientes: {len(self.cola)}")
        self.dibujar()

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if w < 50 or h < 50:
            return

        nombres = list(self.cola.recorrer())
        if not nombres:
            c.create_text(w / 2, h / 2, text="La cola está vacía",
                          fill=AZUL, font=("Segoe UI", 14))
            return

        actual = self.cola.turno_actual()
        n = len(nombres)
        cx, cy = w / 2, h / 2
        textos = [str(x) for x in nombres]

        # Se ajusta la tipografía y el tamaño del óvalo para que el nombre
        # completo siempre quepa (sin recortarlo con "...").
        tam = 11
        while True:
            fuente = tkfont.Font(family="Segoe UI", size=tam, weight="bold")
            ancho = max(fuente.measure(t) for t in textos)
            r_nodo = max(24, ancho / 2 + 10)
            radio = max(40, min(w, h) / 2 - r_nodo - 10)
            cabe = n == 1 or 2 * radio * math.sin(math.pi / n) >= 2 * r_nodo + 16
            if cabe or tam <= 6:
                break
            tam -= 1

        # Posiciones (el primero arriba, sentido horario)
        pos = []
        for i in range(n):
            ang = -math.pi / 2 + 2 * math.pi * i / n
            pos.append((cx + radio * math.cos(ang), cy + radio * math.sin(ang)))

        # Flechas (incluye la de cierre del ciclo: último -> primero)
        # Solo se dibujan flechas cuando hay 2 o más clientes
        if n >= 2:
            for i in range(n):
                x1, y1 = pos[i]
                x2, y2 = pos[(i + 1) % n]
                d = math.hypot(x2 - x1, y2 - y1) or 1
                ux, uy = (x2 - x1) / d, (y2 - y1) / d
                c.create_line(x1 + ux * r_nodo, y1 + uy * r_nodo,
                              x2 - ux * r_nodo, y2 - uy * r_nodo,
                              arrow="last", fill=AZUL, width=2,
                              arrowshape=(10, 12, 5))

        # Nodos
        marcado = False
        for i, nombre in enumerate(nombres):
            x, y = pos[i]
            es_actual = (nombre == actual and not marcado)
            if es_actual:
                marcado = True
            relleno = VERDE if es_actual else AZUL_CLARO
            borde = VERDE_OSCURO if es_actual else AZUL
            color_txt = BLANCO if es_actual else AZUL_OSCURO
            c.create_oval(x - r_nodo, y - r_nodo, x + r_nodo, y + r_nodo,
                          fill=relleno, outline=borde, width=2)
            c.create_text(x, y, text=str(nombre), fill=color_txt, font=fuente)

        c.create_text(cx, cy, text=f"Ronda {self.cola.ronda}", fill=VERDE_OSCURO,
                      font=("Segoe UI", 12, "bold"))


if __name__ == "__main__":
    App().mainloop()
