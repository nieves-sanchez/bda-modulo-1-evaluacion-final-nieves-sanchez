# Tienda Online (V2) — Ejercicio final Módulo 1

Aplicación por consola que simula una tienda online: gestión de inventario, clientes y compras.

Este repositorio contiene dos versiones:

- **V1 (Notebook)**: versión original del ejercicio en `.ipynb`.
- **V2 (Python)**: refactor del proyecto para mejorar el diseño y la legibilidad.

---

## Estructura del repositorio

├─ notebooks/
│ └─ V1_Ejercicio-final-...ipynb
├─ v2/
│ ├─ main.py
│ └─ tienda.py
└─ README.md

- `notebooks/`: entrega original (V1) en Jupyter Notebook.
- `v2/`: versión refactorizada (V2) lista para ejecutar desde terminal.

---

## Objetivo de la V2 (refactor)

Refactorizar el proyecto para que sea más profesional:

- Separar la **interfaz de consola (UI)** de la **lógica de negocio**.
- Normalizar nombres para búsquedas consistentes.
- Validar emails con regex.
- Añadir type hints y docstrings para mejorar legibilidad.
- Corregir y controlar errores frecuentes (duplicados, stock negativo, etc.).

---

## Decisiones de diseño (V2)

### 1) Separación UI / lógica

- **`tienda.py`**: contiene la clase `TiendaOnline` con lógica de negocio **sin `input()` ni `print()`**.
- **`main.py`**: contiene la interfaz por consola (menú, inputs y prints).

Esto hace que la clase sea más reutilizable y mantenible (por ejemplo, si en el futuro se quisiera convertir en una API).

### 2) Normalización de nombres

Para comparar nombres (productos / clientes) se usa:

- `strip()` + `casefold()`

Así se evita que cambios de mayúsculas o espacios afecten a las búsquedas.

### 3) Email: normalización + validación (regex)

- Normalización: `strip()` + `casefold()` para evitar duplicados.
- Validación con regex.

### 4) Type hints + docstrings

Se añadieron Type hints y docstrings para facilitar la comprensión del código y su revisión.

---

## Requisitos

- Python **3.10+** recomendado.
- No requiere librerías externas (solo librerías estándar de Python).

---

## Cómo ejecutar

Desde la raíz del repositorio:

```bash
python v2/main.py
```

---

## Funcionalidades

Menú por consola:

Añadir / actualizar producto

Ver inventario

Buscar producto

Actualizar stock

Eliminar producto

Calcular valor del inventario

Añadir cliente

Ver clientes

Realizar compra (carrito + pago + registro)

Ver compras de un cliente

Flujo de compra (resumen)

La UI (main) construye el carrito (productos y cantidades).

TiendaOnline.realizar_compra() valida cliente, productos y stock, calcula total y descuenta stock.

La UI pide la cantidad entregada y llama a procesar_pago().

Si el pago es correcto, se registra la compra en el historial del cliente con registrar_compra().

## Mejoras futuras (ideas)

Validación “en tiempo real” del nombre del cliente antes de construir el carrito.

Normalización más avanzada (por ejemplo, ignorar tildes/acentos en búsquedas).

Persistencia de datos (CSV / JSON / SQL).
