from datetime import datetime, timedelta
from Productos.models import Producto

class Carrito:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")

        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, producto, cantidad, imagen):
        id = str(producto.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre_producto,
                "tipo": producto.tipo_producto,
                "subtotal": producto.precio_producto * cantidad,
                "modo_venta": producto.modo_venta,
                "stock": producto.stock_producto,
                "descripcion": producto.descripcion_producto,
                "imagen": imagen,
                "cantidad": cantidad,
            }
        else:
            self.carrito[id]["cantidad"] += cantidad
            self.carrito[id]["subtotal"] += producto.precio_producto * cantidad
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["subtotal"] -= producto.precio_producto
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()

    def sumar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["subtotal"] += producto.precio_producto
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    '''def expiracion(self):
        carrito = self.session.get('carrito')
        if len(carrito) > 0:
            inicio_sesion = datetime.now()
            expiracion_carrito = datetime.now()+timedelta(seconds=40)
            while inicio_sesion != expiracion_carrito:
                inicio_sesion = datetime.now()
                if inicio_sesion == expiracion_carrito:
                    for key, value in self.session["carrito"].items():
                        cantidad = self.carrito["cantidad"]
                        producto = Producto.objects.get(id=key)
                        producto.stock_producto += cantidad
                        producto.save()
                        del self.carrito[key]
                        self.guardar_carrito()'''


