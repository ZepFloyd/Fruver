

function actualizarPedido(id) {
    Swal.fire({
        title: 'Seleccione un estado para el pedido:',
        input: 'select',
        inputOptions: {
        'Estados': {
            Recibido: 'Recibido',
            Armado: 'Armado',
            Despachado: 'Despachado',
            Pagado: 'Pagado'
        },
        },
        showCancelButton: true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Aceptar",
        "confirmButtonColor": "green",
    })
    .then(function(result) {
        if(result.isConfirmed) {
            window.location.href = "/pedidos/actualizarpedido/"+id+"/"+result.value
        }
    })
}