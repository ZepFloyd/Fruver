/*función para que aparezca el pop up de crear gasto al presionar el botón añadir gastos del día*/
document.getElementById("creargasto").addEventListener('click',
function() {
    document.querySelector(".popup-creargasto").style.display = 'flex';
});

/*función para que desaparezca el pop up de crear gasto al presionar el botón cancelar*/
document.getElementById("cancelar-creargasto").addEventListener('click',
function() {
    document.querySelector('.popup-creargasto').style.display = 'none';
});



/*función para que aparezca el pop up de crear gasto al presionar el botón añadir gastos del día
document.getElementsByName("otherexpenses")[1].addEventListener('click',
function() {
    document.querySelector(".popup-otrogasto").style.display = 'flex';
});

/*función para que desaparezca el pop up de crear gasto al presionar el botón cancelar
document.getElementById("cancelar-otrogasto").addEventListener('click',
function() {
    document.querySelector('.popup-otrogasto').style.display = 'none';
});
*/


function agregarOtroGasto(id) {
    document.getElementById(id).style.display = 'flex';
}


function cancelarOtroGasto(id) {
    document.getElementById(id).style.display = 'none';
}


function eliminarGasto(id) {
    Swal.fire({
        "title":"¿Realmente desea eliminar este registro?",
        "text":"Recuerde que esta acción también incluye a todos los otros gastos asociados y no se puede deshacer",
        "icon":"warning",
        "showCancelButton":true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Sí, eliminar",
        "confirmButtonColor": "firebrick",
    })
    .then(function(result) {
        if(result.isConfirmed) {
            window.location.href = "/gastos/eliminargasto/"+id
        }
    })
}