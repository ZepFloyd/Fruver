/*función para que aparezca el pop up de crear vendedor al presionar el botón crear nuevo vendedor*/
document.getElementById("crearvendedor").addEventListener('click',
function() {
    document.querySelector(".popup-crearvendedor").style.display = 'flex';
});

/*función para que desaparezca el pop up de crear vendedor al presionar el botón cancelar*/
document.getElementById("cancelar-crearvendedor").addEventListener('click',
function() {
    document.querySelector('.popup-crearvendedor').style.display = 'none';
});


function eliminarVendedor(id) {
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
            window.location.href = "/mainmenu/gestionarvendedor/eliminarvendedor/"+id
        }
    })
}


/*

document.getElementById("editar").addEventListener('click',
function() {
    document.querySelector(".popup-editarvendedor").style.display = 'flex';
});


document.getElementById("cancelar-editarvendedor").addEventListener('click',
function() {
    document.querySelector('.popup-editarvendedor').style.display = 'none';
});


document.getElementById("eliminar").addEventListener('click',
function() {
    document.querySelector(".popup-eliminarvendedor").style.display = 'flex';
});


document.getElementById("cancelar-eliminarvendedor").addEventListener('click',
function() {
    document.querySelector('.popup-eliminarvendedor').style.display = 'none';
});

*/

/* Se agregan los placeholders con javascript y se comienza los queries
en índice 1 porque CSRF_token es el índice 0
(se le considera un input field)*/

//Query en todos input fields
var form_fields = document.getElementsByTagName('input')
form_fields[1].placeholder='ej: Juan';
form_fields[2].placeholder='ej: Pérez';
form_fields[3].placeholder='Mínimo 8 caracteres';
form_fields[4].placeholder='Reingrese su contraseña';
form_fields[5].placeholder='Nueva Av. 561';
form_fields[6].placeholder='ej: micorreo@mail.com';
form_fields[7].placeholder='ej: 56944441111';


for (var field in form_fields){	
form_fields[field].className += 'form-control'}

var select_field = document.getElementsByTagName('select')
select_field.className = 'form-control'