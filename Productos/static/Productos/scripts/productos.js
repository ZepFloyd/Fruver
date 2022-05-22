

/*función para eliminar un producto de la base de datos*/
function eliminarProducto(id) {
    Swal.fire({
        "title":"¿Realmente desea eliminar este producto?",
        "text":"Recuerde que esta acción no se puede deshacer",
        "icon":"warning",
        "showCancelButton":true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Sí, eliminar",
        "confirmButtonColor": "firebrick",
    })
    .then(function(result) {
        if(result.isConfirmed) {
            window.location.href = "/eliminarproducto/"+id
        }
    })
}