

function eliminarCliente(id) {
    Swal.fire({
        "title":"¿Realmente desea eliminar a este usuario?",
        "text":"Recuerde que esta acción no se puede deshacer",
        "icon":"warning",
        "showCancelButton":true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Sí, eliminar",
        "confirmButtonColor": "firebrick",
    })
    .then(function(result) {
        if(result.isConfirmed) {
            window.location.href = "/clientes/eliminarcliente/"+id
        }
    })
}