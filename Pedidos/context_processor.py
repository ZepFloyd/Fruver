
def total_pedido(request):
    subtotal = 0
    total = 0
    iva = 0
    costo_envio = 3500
    
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                subtotal += int(value["subtotal"])
            iva = int((subtotal*19)/119)
            total = subtotal + costo_envio
    
    return {"total_pedido": total, "iva": iva, "costo_envio": costo_envio, "subtotal": subtotal}