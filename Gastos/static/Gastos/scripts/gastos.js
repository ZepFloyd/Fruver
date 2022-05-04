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



/*función para que aparezca el pop up de crear gasto al presionar el botón añadir gastos del día*/
document.getElementById("otherexpenses").addEventListener('click',
function() {
    document.querySelector(".popup-otrogasto").style.display = 'flex';
});

/*función para que desaparezca el pop up de crear gasto al presionar el botón cancelar*/
document.getElementById("cancelar-otrogasto").addEventListener('click',
function() {
    document.querySelector('.popup-otrogasto').style.display = 'none';
});