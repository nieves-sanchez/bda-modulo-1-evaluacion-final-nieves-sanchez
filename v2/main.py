from __future__ import annotations

from tienda import TiendaOnline

# ----------------------------
# HELPERS UI (consola)
# ----------------------------

def pedir_texto(mensaje: str) -> str:
    """Pide un texto no vacío por consola."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Error: no puede estar vacío.")


def pedir_int(mensaje: str, min_val: int | None = None, max_val: int | None = None) -> int:
    """Pide un entero válido por consola, con rango opcional."""
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("Error: introduce un número entero válido.")
            continue

        if min_val is not None and valor < min_val:
            print(f"Error: debe ser >= {min_val}.")
            continue

        if max_val is not None and valor > max_val:
            print(f"Error: debe ser <= {max_val}.")
            continue

        return valor


def pedir_float(mensaje: str, min_val: float | None = None, max_val: float | None = None) -> float:
    """Pide un número decimal válido por consola, con rango opcional."""
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print("Error: introduce un número válido.")
            continue

        if min_val is not None and valor < min_val:
            print(f"Error: debe ser >= {min_val}.")
            continue

        if max_val is not None and valor > max_val:
            print(f"Error: debe ser <= {max_val}.")
            continue

        return valor


# ----------------------------
# MENÚ
# ----------------------------

def mostrar_menu() -> None:
    print("\n--- TIENDA ONLINE ---")
    print("1) Añadir / actualizar producto")
    print("2) Ver inventario")
    print("3) Buscar producto")
    print("4) Actualizar stock")
    print("5) Eliminar producto")
    print("6) Calcular valor inventario")
    print("7) Añadir cliente")
    print("8) Ver clientes")
    print("9) Realizar compra")
    print("10) Ver compras de un cliente")
    print("0) Salir")


def main() -> None:
    tienda = TiendaOnline()

    while True:
        mostrar_menu()
        opcion = pedir_int("Elige una opción: ", min_val=0, max_val=10)

        if opcion == 0:
            print("Saliendo... ¡Hasta luego!")
            break

        if opcion == 1:
            print("\n--- Añadir / actualizar producto ---")
            nombre = pedir_texto("Nombre del producto: ")
            precio = pedir_float("Precio: ", min_val=0)
            cantidad = pedir_int("Cantidad: ", min_val=0)

            ok, mensaje = tienda.agregar_producto(nombre, precio, cantidad)
            print(mensaje)
            
        elif opcion == 2:
            print("\n--- Inventario ---")
            inventario = tienda.ver_inventario()

            if not inventario:
                print("El inventario está vacío.")
            else:
                for producto in inventario:
                    print(
                        f"- {producto['nombre']} | Precio: {producto['precio']} | Stock: {producto['cantidad']}"
                    )

        elif opcion == 3:
            print("\n--- Buscar producto ---")
            nombre = pedir_texto("Nombre del producto a buscar: ")

            producto = tienda.buscar_producto(nombre)
            if producto is None:
                print("Producto no encontrado.")
            else:
                print(
                    f"Nombre: {producto['nombre']}\n"
                    f"Precio: {producto['precio']}\n"
                    f"Stock: {producto['cantidad']}"
                )

        elif opcion == 4:
            print("\n--- Actualizar stock ---")
            nombre = pedir_texto("Nombre del producto: ")
            print("Introduce un número positivo para sumar stock o negativo para restar stock.")
            delta = pedir_int("Cantidad (delta): ")

            ok, mensaje = tienda.actualizar_stock(nombre, delta)
            print(mensaje)

        elif opcion == 5:
            print("\n--- Eliminar producto ---")
            nombre = pedir_texto("Nombre del producto a eliminar: ")

            ok, mensaje = tienda.eliminar_producto(nombre)
            print(mensaje)

        elif opcion == 6:
            print("\n--- Valor del inventario ---")
            inventario = tienda.ver_inventario()

            if not inventario:
                print("El inventario está vacío.")
            else:
                total = tienda.calcular_valor_inventario()
                print(f"El valor total del inventario es: {total:.2f} €")

        elif opcion == 7:
            print("\n--- Añadir cliente ---")
            nombre = pedir_texto("Nombre del cliente: ")
            email = pedir_texto("Email del cliente: ")

            ok, mensaje = tienda.agregar_cliente(nombre, email)
            print(mensaje)
        
        elif opcion == 8:
            print("\n--- Clientes ---")
            clientes = tienda.ver_clientes()

            if not clientes:
                print("No hay clientes registrados.")
            else:
                for c in clientes:
                    print(f"- {c['nombre']} | {c['email']}")

        elif opcion == 9:
            print("\n--- Realizar compra (bloque 1: carrito + total) ---")

            nombre_cliente = pedir_texto("Nombre del cliente: ")

            carrito: dict[str, int] = {}

            while True:
                nombre_producto = input("Nombre del producto (o 'salir' para terminar): ").strip()
                if not nombre_producto:
                    print("Error: el nombre del producto no puede estar vacío.")
                    continue

                if nombre_producto.casefold() == "salir":
                    break

                cantidad = pedir_int("Cantidad: ", min_val=1)

                # Si el producto ya estaba en el carrito, acumulamos
                carrito[nombre_producto] = carrito.get(nombre_producto, 0) + cantidad

            ok, total, detalle, mensaje = tienda.realizar_compra(nombre_cliente, carrito)
            print(mensaje)

            if ok:
                print(f"Total compra: {total:.2f} €")
                print("Detalle:")
                for nombre, info in detalle.items():
                    print(f"- {nombre} | Cantidad: {info['cantidad']} | Precio: {info['precio']}")
                    
                # ---- Bloque 2: pago + registro ----
                cantidad_entregada = pedir_float("Cantidad entregada por el cliente: ", min_val=0)

                ok_pago, cambio, mensaje_pago = tienda.procesar_pago(total, cantidad_entregada)
                print(mensaje_pago)

                if ok_pago:
                    ok_registro, mensaje_registro = tienda.registrar_compra(
                        nombre_cliente, detalle, total
                    )
                    print(mensaje_registro)
                    print(f"Cambio: {cambio:.2f} €")


        elif opcion == 10:
            print("\n--- Compras de un cliente ---")
            nombre_cliente = pedir_texto("Nombre del cliente: ")

            ok, compras, mensaje = tienda.ver_compras_cliente(nombre_cliente)
            print(mensaje)

            if ok:
                if not compras:
                    print("El cliente no tiene compras registradas.")
                else:
                    for i, compra in enumerate(compras, start=1):
                        print(f"\nCompra {i}: Total {compra['total']:.2f} €")
                        for nombre, info in compra["productos"].items():
                            print(
                                f"- {nombre} | Cantidad: {info['cantidad']} | "
                                f"Precio: {info['precio']}"
                            )

if __name__ == "__main__":
    main()
