document.addEventListener("DOMContentLoaded", () => {

renderCart()
updateCartBadge()
updateSummary()

initPayment()
initConfirm()

})


/* ---------------- PAYMENT ---------------- */

function initPayment(){

const radios = document.querySelectorAll('input[name="payment"]')

radios.forEach(radio => {
radio.addEventListener("change", () => changePayment(radio.value))
})

}

function changePayment(method){

const box = document.getElementById("payment-info")
if(!box) return

box.innerHTML = ""

if(method === "PromptPay"){

const box = document.getElementById("payment-info")
if(!box) return

box.innerHTML = `<p class="text-center">Loading...</p>`
setTimeout(() => {

  const cart = JSON.parse(localStorage.getItem("cart")) || []

let subtotal = 0
cart.forEach(item => {
  subtotal += item.price * item.qty
  })
  let vat = subtotal * 0.07
  let total = subtotal + vat

  const phone = "0808757765"
  const qrURL = `/static/home/img/prom.jpg`

box.innerHTML = `
<div class="text-center">
  <img src="${qrURL}" class="w-40 mx-auto mb-3">
  <p>Scan to pay</p>
  <p>$${total}</p>
  <p onclick="navigator.clipboard.writeText('0808757765')" class="cursor-pointer">
    PromptPay: <span class="font-semibold">080-875-7765 (tap to copy)</span>
  </p>
</div>`

}, 500) // ⏳ delay 500ms

}

else if(method === "Cash"){
box.innerHTML = `
<p>Pay with cash at counter</p>`
}

}


/* ---------------- SUMMARY ---------------- */

function updateSummary(){

const cart = JSON.parse(localStorage.getItem("cart")) || []

let subtotal = 0

cart.forEach(item=>{
     subtotal += item.price * item.qty
})
let vat = subtotal * 0.07
let total = subtotal + vat

const subEl = document.getElementById("subtotal")
const vatEl = document.getElementById("vat")
const totalEl = document.getElementById("total")

if(subEl) subEl.innerText = subtotal.toFixed(2)
if(vatEl) vatEl.innerText = vat.toFixed(2)
if(totalEl) totalEl.innerText = total.toFixed(2)

}


/* ---------------- CONFIRM ---------------- */

function initConfirm(){

const btn = document.getElementById("confirm-btn")
if(!btn) return

btn.addEventListener("click", () => {

const payment = document.querySelector('input[name="payment"]:checked')

if(!payment){
alert("Please select payment method")
return
}

confirmOrder()

})

}

async function confirmOrder(){

const cart = JSON.parse(localStorage.getItem("cart")) || []

if(cart.length === 0){
alert("Your cart is empty")
return
}

const payment = document.querySelector('input[name="payment"]:checked')

if(!payment){
alert("Please select payment method")
return
}

const button = document.getElementById("confirm-btn")
if(button) button.disabled = true

try {
  const response = await fetch("/orders/create/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
    },
    body: JSON.stringify({cart, payment: payment.value})
  })
  const result = await response.json()
  if(!response.ok) throw new Error(result.error || "Unable to create order")

  localStorage.removeItem("cart")
  window.location.href = result.redirect_url
} catch(error) {
  alert(error.message)
  if(button) button.disabled = false
}

}