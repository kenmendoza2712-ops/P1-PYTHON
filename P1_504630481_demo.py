"""
Proyecto 1 - BIS08 Estructuras de Datos
Demo del Caso 2: turnos de ventanilla en rondas (lista circular simple).

Cómo ejecutar (en la misma carpeta que P1_<carnet>_estructura.py):
    python P1_<carnet>_demo.py
"""
import glob
import importlib.util
import os

carpeta = os.path.dirname(os.path.abspath(__file__))
ruta = glob.glob(os.path.join(carpeta, "P1_*_estructura.py"))[0]
spec = importlib.util.spec_from_file_location("estructura", ruta)
estructura = importlib.util.module_from_spec(spec)
spec.loader.exec_module(estructura)
ColaTurnosCircular = estructura.ColaTurnosCircular


def titulo(texto):
    print(f"\n=== {texto} ===")


# 1. ESTRUCTURA VACÍA: ninguna operación debe fallar.
titulo("1. Estructura vacía")
q = ColaTurnosCircular()
print("¿Vacía?:", q.esta_vacia(), "| tamaño:", len(q))
print("Turno actual:", q.turno_actual())
print("Atender en vacía:", q.atender_y_avanzar())
print("Eliminar en vacía:", q.eliminar("Ana"))
print("Buscar en vacía:", q.buscar("Ana"))
print("Recorrido:", list(q.recorrer()), "->", q)

# 2. UN SOLO ELEMENTO: el nodo se apunta a sí mismo.
titulo("2. Un solo elemento")
q.insertar_final("Ana")
print(q)
print("Atiende:", q.atender_y_avanzar(), "| ronda ahora:", q.ronda)
print("Atiende otra vez (ella misma en la ronda siguiente):",
      q.atender_y_avanzar(), "| ronda ahora:", q.ronda)
print("Eliminar Ana:", q.eliminar("Ana"), "| ¿vacía?:", q.esta_vacia(),
      "| ronda reiniciada:", q.ronda)

# 3. DATOS REPRESENTATIVOS: varias rondas seguidas.
titulo("3. Rondas sucesivas con 4 clientes")
for cliente in ["Ana", "Beto", "Carla", "Diego"]:
    q.insertar_final(cliente)
print(q)
for i in range(9):
    atendido = q.atender_y_avanzar()
    print(f"Turno {i + 1}: {atendido:6} | ronda en curso: {q.ronda}")
print(q)

# 4. BÚSQUEDA: existente e inexistente.
titulo("4. Búsqueda")
print("¿Está Carla?:", q.buscar("Carla"))
print("¿Está Zoe?:", q.buscar("Zoe"))

# 5. ELIMINACIÓN: turno actual, inexistente, último y primero.
titulo("5. Eliminación y casos de borde")
print("Estado:", q)
quien = q.turno_actual()
print(f"Eliminar a quien tiene el turno ({quien}):", q.eliminar(quien))
print("Turno ahora de:", q.turno_actual(), "|", q)
print("Eliminar inexistente 'Zoe':", q.eliminar("Zoe"))
ultimo = list(q.recorrer())[-1]
print(f"Eliminar el último ({ultimo}):", q.eliminar(ultimo), "|", q)
primero = list(q.recorrer())[0]
print(f"Eliminar el primero ({primero}):", q.eliminar(primero), "|", q)

# 6. CIERRE DEL CICLO: tras eliminar, el ciclo sigue cerrado.
titulo("6. El ciclo sigue cerrado tras eliminar")
for _ in range(4):
    print("Atiende:", q.atender_y_avanzar(), "| ronda:", q.ronda)

# 7. NUEVOS CLIENTES: llegan en medio de las rondas.
titulo("7. Llegan clientes nuevos")
q.insertar_final("Elena")
q.insertar_final("Fabio")
print(q)
print("Recorrido (una sola vuelta):", list(q.recorrer()))
print("Cantidad de clientes:", len(q))
