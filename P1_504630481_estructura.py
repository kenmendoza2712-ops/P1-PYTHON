"""
Proyecto 1 - Estructuras de Datos
Caso 2: Turnos de atención en una ventanilla que se reparten en rondas.

Variante elegida: LISTA CIRCULAR SIMPLE.

Idea general
------------
- Cada cliente se guarda en un Nodo con una única referencia: `siguiente`.
- El último nodo NO apunta a None, sino de vuelta al primero. Así la
  secuencia no tiene un "final": después del último cliente viene el primero
  de la ronda siguiente.
- La estructura guarda solo la referencia al ÚLTIMO nodo (`_ultimo`).
  El primero siempre es `_ultimo.siguiente`, por lo que insertar al final
  de la ronda es inmediato, sin recorrer nada.
- `_actual` apunta al cliente al que le toca el turno.
- `ronda` cuenta cuántas veces el turno ha dado la vuelta completa.
"""


class Nodo:
    """Nodo de la lista: guarda un dato (el cliente) y un enlace al siguiente."""

    def __init__(self, dato):
        self.dato = dato          # información del cliente (nombre, ficha, etc.)
        self.siguiente = None     # referencia al siguiente nodo de la ronda


class ColaTurnosCircular:
    """Lista circular simple que modela las rondas de atención de una ventanilla."""

    def __init__(self):
        self._ultimo = None   # último nodo de la ronda; su `siguiente` es el primero
        self._actual = None   # nodo al que le toca ser atendido
        self._tamano = 0      # cantidad de clientes en la ronda
        self.ronda = 1        # número de ronda en curso


    # Consultas básicas

    def esta_vacia(self):
        """Devuelve True si no hay clientes en la estructura."""
        return self._ultimo is None

    def __len__(self):
        """Cantidad de clientes en la ronda (permite usar len(cola))."""
        return self._tamano

    def turno_actual(self):
        """
        Devuelve el cliente al que le toca, SIN avanzar el turno.
        Si la estructura está vacía devuelve None.
        """
        return None if self._actual is None else self._actual.dato


    # Inserción

    def insertar_final(self, dato):
        """
        Agrega un cliente al final de la ronda (justo antes de volver al primero).

        Casos:
        - Vacía: el nuevo nodo se apunta a sí mismo (ciclo de un solo elemento)
          y pasa a ser el último y el que tiene el turno.
        - Con elementos: se enlazan tres referencias en este orden para no
          perder el primer nodo:
            1) el nuevo apunta al primero (el `siguiente` del último actual),
            2) el último actual apunta al nuevo,
            3) el nuevo pasa a ser el último.
        """
        nuevo = Nodo(dato)

        if self._ultimo is None:                       # caso: estructura vacía
            nuevo.siguiente = nuevo                    # se apunta a sí mismo
            self._ultimo = nuevo
            self._actual = nuevo
        else:                                          # caso: ya hay clientes
            nuevo.siguiente = self._ultimo.siguiente   # 1) nuevo -> primero
            self._ultimo.siguiente = nuevo             # 2) último viejo -> nuevo
            self._ultimo = nuevo                       # 3) nuevo es el último

        self._tamano += 1


    # Avance de turno (operación propia de la variante circular)

    def atender_y_avanzar(self):
        """
        Devuelve el cliente al que le toca y pasa el turno al siguiente.

        Si el cliente atendido era el último, el turno vuelve al primero y
        comienza una nueva ronda (se incrementa `ronda`). El cliente NO se
        elimina: sigue en la estructura para la ronda siguiente. Para sacarlo
        se usa `eliminar`.

        Devuelve None si la estructura está vacía.
        """
        if self._actual is None:                       # caso: vacía
            return None

        atendido = self._actual.dato

        if self._actual is self._ultimo:               # se cierra una ronda
            self.ronda += 1

        self._actual = self._actual.siguiente          # en el último, esto es el primero
        return atendido


    # Búsqueda y recorrido

    def buscar(self, dato):
        """
        Devuelve True si el cliente está en la ronda, False si no.

        Condición de parada: en una lista circular no existe None que marque
        el final, así que se recorre exactamente `_tamano` nodos (una vuelta
        completa). Un `while nodo is not None` aquí sería un ciclo infinito.
        """
        if self._ultimo is None:                       # caso: vacía
            return False

        nodo = self._ultimo.siguiente                  # empieza en el primero
        for _ in range(self._tamano):                  # una sola vuelta
            if nodo.dato == dato:
                return True
            nodo = nodo.siguiente
        return False

    def recorrer(self):
        """
        Generador que entrega los clientes del primero al último, una vez.
        Se detiene tras `_tamano` elementos para no ciclar infinitamente.

        Uso:  for cliente in cola.recorrer(): ...

        Advertencia: no se debe eliminar ningún cliente mientras se recorre
        con este generador; el nodo eliminado quedaría desconectado y el
        recorrido fallaría con AttributeError.
        """
        if self._ultimo is None:                       # caso: vacía, no entrega nada
            return

        nodo = self._ultimo.siguiente                  # primero
        for _ in range(self._tamano):
            yield nodo.dato
            nodo = nodo.siguiente


    # Eliminación

    def eliminar(self, dato):
        """
        Elimina la primera aparición de `dato`.
        Devuelve True si lo eliminó; False si no existe o la estructura está vacía.

        Hay que conocer el nodo ANTERIOR al que se elimina, porque la lista es
        simple (no hay enlace hacia atrás). Se recorre con dos referencias:
        `anterior` y `nodo`. El anterior al primero es el último (por ser circular).

        Casos de borde que se actualizan explícitamente:
        - Único elemento: la estructura queda vacía (todo a None, ronda a 1).
        - Se elimina el último: `_ultimo` pasa a ser el anterior, para que la
          referencia no apunte a un nodo ya desconectado.
        - Se elimina el primero: se resuelve solo, porque el primero siempre
          es `_ultimo.siguiente` y el anterior (el último) salta al segundo.
        - Se elimina a quien tiene el turno: `_actual` pasa al siguiente.
        """
        if self._ultimo is None:                       # caso: vacía
            return False

        anterior = self._ultimo                        # anterior del primero = último
        nodo = self._ultimo.siguiente                  # primero

        # Búsqueda con parada tras una vuelta completa.
        for _ in range(self._tamano):
            if nodo.dato == dato:
                break                                  # encontrado
            anterior = nodo
            nodo = nodo.siguiente
        else:
            return False                               # dio la vuelta: no existe

        if self._tamano == 1:                          # caso: único elemento
            self._ultimo = None
            self._actual = None
            self.ronda = 1                             # sin clientes, se reinicia
        else:
            era_ultimo = nodo is self._ultimo          # se guarda ANTES de actualizar _ultimo
            anterior.siguiente = nodo.siguiente        # el anterior "salta" el nodo
            if era_ultimo:                             # se eliminó el último
                self._ultimo = anterior
            if nodo is self._actual:                   # se eliminó a quien tocaba
                if era_ultimo:                         # el turno da la vuelta: nueva ronda
                    self.ronda += 1
                self._actual = nodo.siguiente

        nodo.siguiente = None                          # evita dejar el nodo enlazado
        self._tamano -= 1
        return True


    # Representación en texto (útil para el demo)

    def __str__(self):
        """
        Muestra la ronda en orden; marca con * al cliente al que le toca.
        Ejemplo: Ana -> Beto* -> Carla -> (vuelve al primero)
        """
        if self._ultimo is None:
            return "(ronda vacía)"

        partes = []
        nodo = self._ultimo.siguiente
        for _ in range(self._tamano):
            marca = "*" if nodo is self._actual else ""
            partes.append(f"{nodo.dato}{marca}")
            nodo = nodo.siguiente
        return " -> ".join(partes) + " -> (vuelve al primero)"
