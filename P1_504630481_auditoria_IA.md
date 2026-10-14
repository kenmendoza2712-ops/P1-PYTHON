# Auditoría de IA – Proyecto 1 (Caso 2, lista circular simple)

El código de `P1_504630481_estructura.py` se generó con un asistente de IA (Claude) durante una conversación de apoyo para este proyecto. La revisión, las pruebas y los hallazgos de este documento son de mi autoría y salen de ejecutar las pruebas y leer el código. El método auditado en detalle es `eliminar`, y además se revisaron todos los demás métodos de la clase.

## 1. Prompt utilizado

Mensaje 1 (con el documento del proyecto adjunto):

> Hola, necesito ayuda para hacer este proyecto, me corresponde el caso  numero dos, la estructura es en python

Mensaje 2:

> ok, vamos por partes, mejor primero dame el script en python para copiarlo y que este documentado en el codigo, porfa

Mensaje 3:

> ok, ya con los archivos, puedes hacerme un cuadro con el paso a paso de lo que debo ir haciendo (Esto porque se me envio el script, pero ademas de eso, se le pidio ayuda para trabajar las otras partes del proyecto)

## 2. Respuesta de la IA 

Método `eliminar` de la clase `ColaTurnosCircular`, tal como lo entregó la IA, antes de aplicar la corrección:

```python
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
            anterior.siguiente = nodo.siguiente        # el anterior "salta" el nodo
            if nodo is self._ultimo:                   # se eliminó el último
                self._ultimo = anterior
            if nodo is self._actual:                   # se eliminó a quien tocaba
                self._actual = nodo.siguiente

        nodo.siguiente = None                          # evita dejar el nodo enlazado
        self._tamano -= 1
        return True
```

## 3. Hallazgos de la revisión

Pruebas usadas como evidencia: `auditoria_completa.py` (secciones [1] a [10] de su salida). Se ejecutó dos veces: antes de la corrección (hallazgo en la sección [8]) y después (todo `OK` en la sección [8]).

| # | Qué se revisó | Resultado | Evidencia (línea o prueba) | Corrección aplicada |
|---|---|---|---|---|
| 1 | `insertar_final`: enlaces del nuevo nodo, `_ultimo` y turno | Correcto | Las líneas `nuevo.siguiente = self._ultimo.siguiente`, `self._ultimo.siguiente = nuevo` y `self._ultimo = nuevo` actualizan los tres enlaces, y en vacía `nuevo.siguiente = nuevo` hace que el nodo se apunte a sí mismo. Sección [2] de la salida: el ciclo queda cerrado y el turno no cambia al insertar. | Ninguna |
| 2 | `atender_y_avanzar`: vacía, un solo elemento y cierre de ronda | Correcto | `if self._actual is None: return None` cubre la vacía, y `if self._actual is self._ultimo: self.ronda += 1` cuenta el cierre de ronda. Sección [3]: 7 turnos dan A,B,C,A,B,C,A; con un elemento se atiende a sí mismo y la ronda sube. | Ninguna |
| 3 | `buscar`: condición de parada | Correcto | Usa `for _ in range(self._tamano)` y no `while`, así que recorre una sola vuelta y no puede ciclar. Sección [4]: el inexistente termina y devuelve `False`. | Ninguna |
| 4 | `recorrer` y `__str__` | Correcto | Ambos usan `for _ in range(self._tamano)`. `__str__` marca el turno con `nodo is self._actual`. Sección [5]: una sola vuelta, vacía sin fallar, y marca un único turno aunque haya nombres repetidos. | Ninguna |
| 5 | `eliminar`: estructura vacía | Correcto | `if self._ultimo is None: return False`. Sección [6]: devuelve `False` sin fallar. | Ninguna |
| 6 | `eliminar`: un solo elemento | Correcto | `if self._tamano == 1:` deja `_ultimo` y `_actual` en `None` y reinicia la ronda. Sección [6]: queda vacía y se puede volver a insertar. | Ninguna |
| 7 | `eliminar`: elemento inexistente | Correcto | El `for ... else: return False` devuelve `False` tras una vuelta completa sin modificar nada. Sección [6]: la lista queda intacta. | Ninguna |
| 8 | `eliminar`: primer nodo (inicio) | Correcto | `anterior = self._ultimo` hace que, al eliminar el primero, el último pase a apuntar al segundo. Sección [6], prueba del primero con 2 y 3 elementos. | Ninguna |
| 9 | `eliminar`: nodo del medio | Correcto | `anterior.siguiente = nodo.siguiente` salta el nodo. Sección [6], prueba del medio. | Ninguna |
| 10 | `eliminar`: último nodo (fin) | Correcto | `self._ultimo = anterior` actualiza la referencia al último; sin esa línea quedaría apuntando a un nodo desconectado. Sección [6], prueba del último con 2 y 3 elementos. | Ninguna |
| 11 | `eliminar`: condición de parada | Correcto | La búsqueda usa `for _ in range(self._tamano)` con `else`, así que no puede entrar en un ciclo infinito en la lista circular. | Ninguna |
| 12 | `eliminar` y el turno (`_actual`) | Correcto | `if nodo is self._actual: self._actual = nodo.siguiente` evita que el turno quede en un nodo borrado. Sección [7]: el turno pasa al siguiente. | Ninguna |
| 13 | Contador de rondas al eliminar al último nodo cuando tenía el turno | **Incorrecto** | Sección [8] antes de corregir: atendiendo al último la ronda sube a 2, pero eliminándolo se quedaba en 1, aunque en ambos casos el turno vuelve al primero. | Agregué `era_ultimo = nodo is self._ultimo` antes de actualizar `_ultimo` y `self.ronda += 1` cuando se elimina al último con el turno. Después: ronda 2 en ambos casos (sección [8] en `OK`). |
| 14 | Referencias y `_tamano` | Correcto | `nodo.siguiente = None` desconecta el nodo eliminado y `self._tamano -= 1` solo se ejecuta cuando se elimina. La función `cerrada()` y la comparación `len(q) == _tamano` se cumplieron en todas las pruebas. | Ninguna |
| 15 | Eliminar mientras se recorre con `recorrer()` | **Riesgoso** | Sección [9]: `AttributeError`, porque `eliminar` deja el `siguiente` del nodo borrado en `None` y el generador sigue sobre ese nodo. | No se corrigió: el caso 2 no pide eliminar durante un recorrido, y quitar `nodo.siguiente = None` dejaría el nodo borrado enlazado. Se documentó la advertencia en el docstring de `recorrer`. |
| 16 | Nombres repetidos al eliminar | **Riesgoso (limitación de diseño)** | Sección [9], nota: se elimina la primera aparición, que no necesariamente es la del cliente que tiene el turno. | No se cambió el código; se documenta como limitación en esta auditoría. |
| 17 | Prueba aleatoria contra un modelo de comparación | Correcto | Sección [10]: 2000 secuencias aleatorias de insertar, atender y eliminar coinciden con el modelo, sin fallos. | Ninguna |

## 4. Conclusión

El código generado por la IA pasó las pruebas de casos de borde (vacía, un solo elemento, elemento inexistente, inicio y fin) y mantuvo la lista circular cerrada en todas las operaciones. Al auditarlo encontré una inconsistencia real en el contador de rondas al eliminar al último cliente cuando tenía el turno, que corregí y volví a comprobar con las mismas pruebas. Quedaron dos limitaciones que decidí documentar y no cambiar: eliminar durante un recorrido y los nombres repetidos.

## Apéndice A. Salida de las pruebas

Script usado: `auditoria_completa.py` (pruebas escritas con apoyo de IA, ejecutadas por mí).

**A.1 Antes de la corrección** (hallazgo en la sección [8])

```
[1] esta_vacia / __len__ / turno_actual
OK       recién creada
OK       tras insertar

[2] insertar_final
OK       en vacía: el nodo se apunta a sí mismo
OK       segundo: orden A,B y ciclo cerrado
OK       tercero: orden A,B,C y ciclo cerrado
OK       el turno no cambia al insertar
OK       nuevo cliente con el turno en el último: sigue C, D, A | ['C', 'D', 'A']

[3] atender_y_avanzar
OK       en vacía devuelve None
OK       un solo elemento: se atiende a sí mismo y la ronda sube cada vez | A,A, ronda=3
OK       3 clientes, 7 turnos: A,B,C,A,B,C,A | ['A', 'B', 'C', 'A', 'B', 'C', 'A']
OK       ronda correcta (3 vueltas completas -> ronda 3 al empezar la tercera) | ronda=3
OK       atender no elimina a nadie

[4] buscar
OK       en vacía
OK       existente (primero, medio, último)
OK       inexistente (termina, no cicla)
OK       buscar no modifica la estructura

[5] recorrer y __str__
OK       recorrer vacía
OK       recorrer una sola vuelta
OK       __str__ vacía
OK       __str__ marca el turno con *
OK       __str__ con nombres repetidos marca solo uno | X* -> X -> (vuelve al primero)

[6] eliminar (casos de borde)
OK       vacía
OK       1 elemento, existe
OK       1 elemento, no existe
OK       2 elementos, primero
OK       2 elementos, último
OK       3 elementos, medio
OK       3 elementos, primero
OK       3 elementos, último
OK       3 elementos, inexistente
OK       vaciar todo y reutilizar
OK       insertar tras vaciar

[7] eliminar y el turno
OK       eliminar a quien tiene el turno (medio): pasa al siguiente
OK       eliminar a otro: el turno no cambia
OK       eliminar al último con el turno: vuelve al primero

[8] coherencia del contador de rondas
HALLAZGO el turno vuelve al primero y la ronda es igual atendiendo o eliminando al último | atendiendo: ronda 2 | eliminando: ronda 1

[9] riesgos de uso
HALLAZGO eliminar durante un recorrido | AttributeError: 'NoneType' object has no attribute 'dato'
NOTA      con nombres repetidos, eliminar quita la PRIMERA aparición, no necesariamente la del turno | B -> A* -> (vuelve al primero)

[10] prueba aleatoria contra un modelo con list (solo para comparar)
OK       2000 secuencias aleatorias de insertar/atender/eliminar coinciden con el modelo | fallos: 0
```

**A.2 Después de la corrección** (sección [8] en `OK`)

```
[1] esta_vacia / __len__ / turno_actual
OK       recién creada
OK       tras insertar

[2] insertar_final
OK       en vacía: el nodo se apunta a sí mismo
OK       segundo: orden A,B y ciclo cerrado
OK       tercero: orden A,B,C y ciclo cerrado
OK       el turno no cambia al insertar
OK       nuevo cliente con el turno en el último: sigue C, D, A | ['C', 'D', 'A']

[3] atender_y_avanzar
OK       en vacía devuelve None
OK       un solo elemento: se atiende a sí mismo y la ronda sube cada vez | A,A, ronda=3
OK       3 clientes, 7 turnos: A,B,C,A,B,C,A | ['A', 'B', 'C', 'A', 'B', 'C', 'A']
OK       ronda correcta (3 vueltas completas -> ronda 3 al empezar la tercera) | ronda=3
OK       atender no elimina a nadie

[4] buscar
OK       en vacía
OK       existente (primero, medio, último)
OK       inexistente (termina, no cicla)
OK       buscar no modifica la estructura

[5] recorrer y __str__
OK       recorrer vacía
OK       recorrer una sola vuelta
OK       __str__ vacía
OK       __str__ marca el turno con *
OK       __str__ con nombres repetidos marca solo uno | X* -> X -> (vuelve al primero)

[6] eliminar (casos de borde)
OK       vacía
OK       1 elemento, existe
OK       1 elemento, no existe
OK       2 elementos, primero
OK       2 elementos, último
OK       3 elementos, medio
OK       3 elementos, primero
OK       3 elementos, último
OK       3 elementos, inexistente
OK       vaciar todo y reutilizar
OK       insertar tras vaciar

[7] eliminar y el turno
OK       eliminar a quien tiene el turno (medio): pasa al siguiente
OK       eliminar a otro: el turno no cambia
OK       eliminar al último con el turno: vuelve al primero

[8] coherencia del contador de rondas
OK       el turno vuelve al primero y la ronda es igual atendiendo o eliminando al último | atendiendo: ronda 2 | eliminando: ronda 2

[9] riesgos de uso
HALLAZGO eliminar durante un recorrido | AttributeError: 'NoneType' object has no attribute 'dato'
NOTA      con nombres repetidos, eliminar quita la PRIMERA aparición, no necesariamente la del turno | B -> A* -> (vuelve al primero)

[10] prueba aleatoria contra un modelo con list (solo para comparar)
OK       2000 secuencias aleatorias de insertar/atender/eliminar coinciden con el modelo | fallos: 0
```

