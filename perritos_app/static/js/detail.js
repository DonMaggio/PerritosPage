function changePhoto(photoUrl) {
    document.getElementById('main-photo').src = photoUrl;
}


function redirectToItem(itemId) {
    console.log("Redirecting to item:", itemId); 
    window.location.href = '/perro/update/'+itemId ; // Asumiendo que la URL espera un ID
}