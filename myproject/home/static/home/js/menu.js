function filterMenu(category){

    const grid = document.getElementById("menu-grid")
    if(!grid) return

    grid.innerHTML = ""

    const filtered = products.filter(p => p.category === category)

    if(filtered.length === 0){
        grid.innerHTML = "<p>ไม่มีเมนู</p>"
        return
    }

    filtered.forEach(product => {
        grid.innerHTML += createCard(product)
    })

}

function renderAllMenu(){

    const grid = document.getElementById("menu-grid")
    if(!grid) return

    grid.innerHTML = ""

    if(!products || products.length === 0){
        grid.innerHTML = "<p>ไม่มีสินค้า</p>"
        return
    }

    products.forEach(product => {
        grid.innerHTML += createCard(product)
    })

}

function setActive(button){

    document.querySelectorAll(".menu-btn")
    .forEach(btn => btn.classList.remove("active"))

    button.classList.add("active")

}

// โหลดหน้า
document.addEventListener("DOMContentLoaded", () => {

    console.log("MENU LOADED", products) // 🔥 debug

    renderAllMenu()

    updateCartBadge()

})