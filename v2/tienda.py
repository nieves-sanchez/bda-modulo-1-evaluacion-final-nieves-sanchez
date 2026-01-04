import re

class TiendaOnline:
    
    def __init__(self):
        self.inventario = []
        self.ventas_totales = 0.0
        self.clientes = {}


# MÉTODOS INTERNOS (HELPERS)
# Estos métodos se utilizan internamente dentro de la clase para evitar repetir 
# código y facilitar la comparación y búsqueda de productos en el inventario.
        
    def _normalizar_nombre(self, texto: str) -> str:
        """Normaliza texto para comparar (strip + casefold)"""
        return texto.strip().casefold()
         
    def _buscar_producto(self, nombre: str) -> dict | None:
        """Busca un producto por nombre (comparación normalizada). Devuelve el diccionario o None"""
        nombre_normalizado = self._normalizar_nombre(nombre)
        
        for producto in self.inventario:
            nombre_producto = self._normalizar_nombre(producto['nombre'])
            if nombre_producto == nombre_normalizado:
                return producto
        
        return None        
    
        
# MÉTODOS INTERNOS DE INPUT (HELPERS)
# Normalizan y validan emails usando regex

    def _email_normalizado(self, email: str) -> str:
        return email.strip().casefold()
    
    def _email_valido(self, email: str) -> bool:
        patron = r"^[^\s@]+@[^\s@]+\.[a-z]{2,10}$"
        return re.match(patron, email.strip().casefold()) is not None
    
    
        

    def agregar_producto(self, nombre: str, precio: float, cantidad: int) -> tuple[bool, str]:
        """
        Añade un producto al inventario o actualiza uno existente.

        Flujo:
        - Valida datos de entrada (nombre no vacío, precio y cantidad no negativos).
        - Busca el producto por nombre normalizado.
        - Si existe:
            - Actualiza precio.
            - Suma la cantidad al stock existente.
        - Si no existe:
            - Crea un nuevo producto y lo añade al inventario.
            - Devuelve (ok, mensaje) para que la UI lo muestre.
        """
        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            return False, "Error: El nombre del producto no puede estar vacío"
        
        if precio < 0:
            return False, "Error: El precio no puede ser negativo"
        
        if cantidad < 0:
            return False, "Error: la cantidad no puede ser negativa"
        
        producto = self._buscar_producto(nombre_limpio)
        
        if producto is not None:
            producto["precio"] = precio
            producto["cantidad"] += cantidad
            
            return True, f"Producto '{producto['nombre']}' actualizado correctamente"     
        
        producto_nuevo = {
            "nombre": nombre_limpio,
            "precio": precio,
            "cantidad": cantidad
        }
        
        self.inventario.append(producto_nuevo)
        return True, f"Producto '{nombre_limpio}' añadido correctamente" 
    
     
    def ver_inventario(self) -> list[dict]:
        """
        Devuelve una copia del inventario (lista de diccionarios) para consulta desde la UI.

        Flujo:
        - Recorre la lista de productos del inventario.
        - Devuelve una lista de diccionarios con nombre, precio y cantidad.
        - Si el inventario está vacío, devuelve una lista vacía.
        """
        return [producto.copy() for producto in self.inventario]
            
               
    def buscar_producto(self, nombre: str) -> dict | None:
        """
        Busca un producto por nombre.

        Flujo:
        - Normaliza el nombre para la búsqueda.
        - Usa el método interno _buscar_producto.
        - Si existe, devuelve el producto.
        - Si no existe, devuelve None.
        """
        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            return None
        
        return self._buscar_producto(nombre_limpio)
    
                    
    def actualizar_stock(self, nombre: str, cantidad: int) -> tuple[bool, str]:
        """
        Actualiza el stock de un producto existente.

        Flujo:
        - Limpia el nombre de entrada.
        - Busca el producto en el inventario.
        - Calcula el nuevo stock sumando la cantidad (puede ser positiva o negativa).
        - Evita que el stock final quede en negativo.
        - Actualiza el stock si todo es correcto.
        - Devuelve (ok, mensaje) para que la UI lo muestre.
        """
        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            return False, "Error: el nombre del producto no puede estar vacío."

        producto = self._buscar_producto(nombre_limpio)
        if producto is None:
            return False, f"El producto '{nombre_limpio}' no existe."

        stock_actual = producto["cantidad"]
        stock_final = stock_actual + cantidad

        if stock_final < 0:
            return (
                False,
                f"Error: el stock actual de '{producto['nombre']}' es {stock_actual}. "
                "No puede quedar en negativo."
            )

        producto["cantidad"] = stock_final
        return True, (
            f"Stock actualizado correctamente para '{producto['nombre']}'. "
            f"{stock_actual} -> {stock_final}"
        )
      
        
    def eliminar_producto(self, nombre: str) -> tuple[bool, str]:
        """
        Elimina un producto del inventario si existe.

        Flujo:
        - Limpia el nombre de entrada.
        - Busca el producto en el inventario.
        - Si no existe, devuelve (False, mensaje).
        - Si existe, lo elimina y devuelve (True, mensaje).
        """
        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            return False, "Error: el nombre del producto no puede estar vacío."

        producto = self._buscar_producto(nombre_limpio)
        if producto is None:
            return False, "Producto no encontrado."

        self.inventario.remove(producto)
        return True, f"Producto '{producto['nombre']}' eliminado correctamente."
     
    
    def calcular_valor_inventario(self) -> float:
        """
        Calcula el valor total del inventario.

        Flujo:
        - Recorre todos los productos del inventario.
        - Suma precio * cantidad de cada producto.
        - Devuelve el total como float.
        - Si el inventario está vacío, devuelve 0.0.
        """
        total = 0.0

        for producto in self.inventario:
            total += producto["precio"] * producto["cantidad"]

        return total

    

    def agregar_cliente(self, nombre: str, email: str) -> tuple[bool, str]:
        """
        Registra un cliente nuevo si no existe, evitando duplicados por nombre y por email.

        Flujo:
        - Limpia/valida datos de entrada.
        - Normaliza nombre para comparación (insensible a mayúsculas/espacios extremos).
        - Normaliza email para comparación (strip + casefold).
        - Comprueba duplicados: mismo nombre (normalizado) o mismo email (normalizado).
        - Si todo ok, guarda el cliente con su email normalizado y una lista de compras vacía.
        - Devuelve (ok, mensaje) para que la UI lo imprima.
        """
        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            return False, "Error: El nombre no puede estar vacío."
        
        email_norm = self._email_normalizado(email)
        if not self._email_valido(email_norm):
            return False, "Error: email no válido."
        
        nombre_key = self._normalizar_nombre(nombre_limpio)
        
        for nombre_existente, datos in self.clientes.items():
            if self._normalizar_nombre(nombre_existente) == nombre_key:
                return False, f"El nombre del cliente '{nombre_existente}' ya existe."
            if datos['email'] == email_norm:
                return False, f"El email '{email_norm}' ya está registrado"
        
        self.clientes[nombre_limpio] = {"email": email_norm, "compras": []}
        return True, f"Cliente '{nombre_limpio}' añadido correctamente"        
        

    def ver_clientes(self) -> list[dict]:
        """
        Devuelve la lista de clientes registrados.

        Flujo:
        - Recorre el diccionario de clientes.
        - Construye una lista con nombre y email de cada cliente.
        - Si no hay clientes, devuelve una lista vacía.
        """
        resultado = []
        
        for nombre, datos in self.clientes.items():
            resultado.append({
                "nombre": nombre,
                "email": datos["email"]
            })
        
        return resultado
            
    def realizar_compra(self, nombre_cliente: str, carrito: dict[str, int]) -> tuple[bool, float, dict, str]:
        """
        Realiza una compra (negocio puro): valida cliente, valida carrito, valida stock,
        descuenta stock y calcula total.

        Flujo:
        - Limpia el nombre del cliente y comprueba que existe.
        - Valida que el carrito no esté vacío y que las cantidades sean enteros > 0.
        - Para cada producto del carrito:
            - Comprueba que exista en inventario.
            - Comprueba stock suficiente.
        - Si todo es correcto:
            - Descuenta stock de TODOS los productos.
            - Calcula el total.
            - Devuelve (ok, total, detalle_carrito, mensaje).
        """
        nombre_limpio = nombre_cliente.strip()
        if nombre_limpio == "":
            return False, 0.0, {}, "Error: el nombre del cliente no puede estar vacío."

        if nombre_limpio not in self.clientes:
            return False, 0.0, {}, "Cliente no encontrado. Regístrate primero."

        if not carrito:
            return False, 0.0, {}, "Carrito vacío."

        detalle = {}
        total = 0.0

        # 1) Validación completa (sin tocar stock aún)
        for nombre_producto, cantidad in carrito.items():
            if not isinstance(cantidad, int) or cantidad <= 0:
                return False, 0.0, {}, f"Cantidad inválida para '{nombre_producto}'."

            producto = self._buscar_producto(nombre_producto)
            if producto is None:
                return False, 0.0, {}, f"Producto no encontrado: '{nombre_producto}'."

            stock_disponible = producto["cantidad"]
            if cantidad > stock_disponible:
                return False, 0.0, {}, (
                    f"Stock insuficiente para '{producto['nombre']}'. "
                    f"Disponible: {stock_disponible}, solicitado: {cantidad}."
                )

            precio = producto["precio"]
            detalle[producto["nombre"]] = {"precio": precio, "cantidad": cantidad}
            total += precio * cantidad

        # 2) Aplicación (descontamos stock)
        for nombre_real, info in detalle.items():
            producto = self._buscar_producto(nombre_real)
            if producto is not None:
                producto["cantidad"] -= info["cantidad"]

        return True, total, detalle, "Compra realizada correctamente."

    
    def procesar_pago(self, total_compra: float, cantidad_entregada: float) -> tuple[bool, float, str]:
        """
        Procesa el pago de una compra.

        Flujo:
        - Valida que total_compra y cantidad_entregada no sean negativos.
        - Si la cantidad entregada es suficiente:
            - Calcula el cambio.
            - Devuelve (True, cambio, mensaje).
        - Si es insuficiente:
            - Devuelve (False, 0.0, mensaje).
        """
        if total_compra < 0:
            return False, 0.0, "Error: el total de la compra no puede ser negativo."

        if cantidad_entregada < 0:
            return False, 0.0, "Error: la cantidad entregada no puede ser negativa."

        if cantidad_entregada >= total_compra:
            cambio = cantidad_entregada - total_compra
            return True, cambio, "Pago realizado correctamente."
        else:
            return False, 0.0, "El importe entregado es insuficiente."

        
        
    def registrar_compra(self, nombre_cliente: str, carrito: dict[str, dict[str, float | int]], total: float) -> tuple[bool, str]:
        """
        Registra una compra en el historial del cliente y acumula las ventas totales.

        Flujo:
        - Comprueba que el cliente exista.
        - Valida que el carrito no esté vacío y que el total sea coherente.
        - Añade la compra al historial del cliente.
        - Suma el total a ventas_totales.
        - Devuelve (ok, mensaje) para que la UI lo muestre.
        """
        nombre_limpio = nombre_cliente.strip()
        if nombre_limpio == "":
            return False, "Error: el nombre del cliente no puede estar vacío."

        if nombre_limpio not in self.clientes:
            return False, "Error: cliente no encontrado."

        if not carrito:
            return False, "Error: carrito vacío."

        if total < 0:
            return False, "Error: el total no puede ser negativo."

        self.clientes[nombre_limpio]["compras"].append({
            "productos": carrito,
            "total": total
        })

        self.ventas_totales += total
        return True, "Compra registrada correctamente."
    

    def ver_compras_cliente(self, nombre_cliente: str) -> tuple[bool, list, str]:
        """
        Devuelve todas las compras realizadas por un cliente.

        Flujo:
        - Limpia el nombre del cliente.
        - Comprueba que exista.
        - Devuelve (ok, compras, mensaje).
        - compras es una lista de dicts con 'productos' y 'total'.
        """
        nombre_limpio = nombre_cliente.strip()
        if nombre_limpio == "":
            return False, [], "Error: el nombre del cliente no puede estar vacío."

        if nombre_limpio not in self.clientes:
            return False, [], "Error: cliente no encontrado."

        compras = self.clientes[nombre_limpio]["compras"]
        return True, compras, "Compras obtenidas correctamente."
