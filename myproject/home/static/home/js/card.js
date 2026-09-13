function createCard(product){

let optionsHTML = ""

// 🍜
if(product.type === "noodle"){
  optionsHTML = `
    <label class="text-sm text-gray-500">Rice Noodles:</label>
    <select id="noodle-${product.id}" class="w-full mt-1 border rounded-lg px-3 py-2">
      <option value="Thin">Thin</option>
      <option value="Wide">Wide</option>
      <option value="egg noodles">egg noodles</option>
    </select>

    <label class="flex items-center gap-2 text-sm bg-green-100 px-3 py-1 rounded-full w-fit">
      <input type="checkbox" id="egg-${product.id}">
      Add an egg (+10$)
    </label>
  `
}

// snacks
else if(product.type === "snacks"){
  optionsHTML = `
    <label class="text-sm text-gray-500"></label>
    <label class="flex items-center gap-2 text-sm">
      <div class="flex items-center gap-1 px-3 py-1 rounded-full">

    </label>
  `
}

// drink
else if(product.type === "drink"){
  optionsHTML = `
    <label class="text-sm text-gray-500"></label>
    <label class="flex items-center gap-2 text-sm">
      <div class="flex items-center gap-1 px-3 py-1 rounded-full">

    </label>
  `
}


// 🍚
else if(product.type === "rice"){
  optionsHTML = `
    <label class="text-sm text-gray-500"></label>
    <label class="flex items-center gap-2 text-sm">
      <div class="flex items-center gap-1 px-3 py-1 rounded-full">

    </label>
  `
}

// 🍜🍚
else if(product.type === "both"){
  optionsHTML = `
    <label class="text-sm text-gray-500">Rice Noodles:</label>
    <select id="noodle-${product.id}" class="w-full mt-1 border rounded-lg px-3 py-2">
      <option value="Thin">Thin</option>
      <option value="Wide">Wide</option>
      <option value="egg noodles">egg noodles</option>
    </select>

    <label class="flex items-center gap-2 text-sm bg-green-100 px-3 py-1 rounded-full w-fit">
      <input type="checkbox" id="egg-${product.id}">
      Add an egg (+10$)
    </label>
  `
}

return `
<article class="h-full min-w-0 p-2">
  <div class="h-full min-w-0 min-h-[420px] bg-white rounded-2xl border border-gray-200 shadow-sm
  hover:shadow-xl hover:-translate-y-1 transition duration-300 overflow-hidden relative flex flex-col">
    <div class="h-44 shrink-0 overflow-hidden bg-black">
      <img src="${product.image}" class="w-full h-full object-cover transition duration-300 hover:scale-105" alt="${product.name}">
    </div>

    <div class="p-4 flex flex-col flex-1">
      <h3 class="min-h-[3.5rem] text-base font-semibold leading-6 text-gray-800">${product.name}</h3>
      <p class="text-orange-500 font-bold text-lg">$ ${product.price}</p>
      <div class="mt-2 min-h-[88px] text-sm text-left space-y-2">${optionsHTML}</div>

      <div class="flex items-center justify-between gap-3 mt-auto pt-4">
        <div class="flex items-center bg-gray-100 rounded-full px-3 py-1 gap-3">
          <button type="button" onclick="decreaseQty(${product.id})" aria-label="Decrease quantity">-</button>
          <span id="qty-${product.id}" class="w-6 text-center">1</span>
          <button type="button" onclick="increaseQty(${product.id})" aria-label="Increase quantity">+</button>
        </div>
        <button type="button" onclick="addToCart(${product.id})" class="bg-orange-500 text-white px-5 py-2 rounded-full hover:bg-orange-600 transition transform hover:scale-105 active:scale-95">Add</button>
      </div>
    </div>

    ${product.popular ? `<span class="absolute top-3 left-3 bg-orange-500 text-white text-xs px-3 py-1 rounded-full shadow">🔥 Hot</span>` : ""}
  </div>
</article>
`
}

// qty
function increaseQty(id){
    let el = document.getElementById(`qty-${id}`)
    el.innerText = parseInt(el.innerText) + 1
}

function decreaseQty(id){
    let el = document.getElementById(`qty-${id}`)
    let qty = parseInt(el.innerText)
    if(qty > 1){
        el.innerText = qty - 1
    }
}

// add cart
function addToCart(id){

const product = products.find(p => p.id === id)
if(!product) return

const qty = parseInt(document.getElementById(`qty-${id}`).innerText)

const noodleEl = document.getElementById(`noodle-${id}`)
const eggEl = document.getElementById(`egg-${id}`)

const noodle = noodleEl ? noodleEl.value : ""
const egg = eggEl ? eggEl.checked : false

const key = `${id}-${noodle}-${egg}`

let cart = JSON.parse(localStorage.getItem("cart")) || []

let existing = cart.find(item => item.key === key)

if(existing){
    existing.qty += qty
}else{
    cart.push({
        ...product,
        qty,
        noodle,
        egg,
        key
    })
}

localStorage.setItem("cart", JSON.stringify(cart))

// reset qty
document.getElementById(`qty-${id}`).innerText = 1

updateCartBadge()
renderCart()
  if (typeof updateSummary === "function") updateSummary()
}

// render cart
function renderCart(){

const cartContainer = document.getElementById("cart-items")
if(!cartContainer) return

const cart = JSON.parse(localStorage.getItem("cart")) || []

cartContainer.innerHTML = ""

let total = 0

cart.forEach(item => {

const extra = item.egg ? 10 : 0
const price = item.price + extra

total += price * item.qty

cartContainer.innerHTML += `
<div class="flex items-center justify-between bg-white p-4 rounded-xl shadow">

    <div>
        <h3>${item.name}</h3>
        <p>
          ${item.type ? item.type : ""}
          ${item.noodle ? item.noodle : ""}
          ${item.egg ? "+ไข่" : ""}
        </p>
        <p>$${price}</p>
    </div>

    <div class="flex items-center gap-3">
        <button onclick="decreaseItem('${item.key}')">-</button>
        <span>${item.qty}</span>
        <button onclick="increaseItem('${item.key}')">+</button>
        <button onclick="removeItem('${item.key}')">🗑️</button>
    </div>

</div>
`
})

// กัน error
const totalEl = document.getElementById("grand-total")
if(totalEl){
  totalEl.innerText = "$ " + total.toFixed(2)
}
}

// increase
function increaseItem(key){
  let cart = JSON.parse(localStorage.getItem("cart")) || []
  const item = cart.find(p => p.key === key)
  if(item) item.qty++
  localStorage.setItem("cart", JSON.stringify(cart))
  renderCart()
  updateCartBadge()
  if (typeof updateSummary === "function") updateSummary()
}

// decrease
function decreaseItem(key){
  let cart = JSON.parse(localStorage.getItem("cart")) || []
  const item = cart.find(p => p.key === key)
  if(item && item.qty > 1){
    item.qty--
  }
  localStorage.setItem("cart", JSON.stringify(cart))
  renderCart()
  updateCartBadge()
  if (typeof updateSummary === "function") updateSummary()
}

// remove
function removeItem(key){
  let cart = JSON.parse(localStorage.getItem("cart")) || []
  cart = cart.filter(item => item.key !== key)
  localStorage.setItem("cart", JSON.stringify(cart))
  renderCart()
  updateCartBadge()
  if (typeof updateSummary === "function") updateSummary()
}

// badge
function updateCartBadge(){

const cart = JSON.parse(localStorage.getItem("cart")) || []

let totalQty = 0
cart.forEach(item => totalQty += item.qty)

const badge = document.getElementById("cart-badge")
if(!badge) return

if(totalQty > 0){
    badge.innerText = totalQty
    badge.classList.remove("hidden")
}else{
    badge.classList.add("hidden")
}
}

// โหลด
renderCart()
updateCartBadge()
updateSummary() 