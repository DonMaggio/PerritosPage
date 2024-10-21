function redirectToItem(itemId) {
    console.log("Redirecting to item:", itemId); 
    window.location.href = '/perro/'+itemId ; // Asumiendo que la URL espera un ID
}