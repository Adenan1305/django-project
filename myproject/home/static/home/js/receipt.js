document.addEventListener("DOMContentLoaded", () => {

    const order = JSON.parse(localStorage.getItem("lastOrder")) || []

    const container = document.getElementById("receipt-items")

    if (!container) return

    let subtotal = 0
    container.innerHTML = ""

    order.forEach(item => {

        const extra = item.egg ? 10 : 0
        const price = item.price + extra

        subtotal += price * item.qty

        container.innerHTML += `
        <div class="flex justify-between">
            <span>${item.name} x${item.qty}</span>
            <span>$${(price * item.qty).toFixed(2)}</span>
        </div>
        `
    })

    const vat = subtotal * 0.07
    const total = subtotal + vat

    document.getElementById("subtotal").innerText = subtotal.toFixed(2)
    document.getElementById("vat").innerText = vat.toFixed(2)
    document.getElementById("total").innerText = total.toFixed(2)

    // payment
    const payment = localStorage.getItem("payment")
    document.getElementById("payment-method").innerText = payment || "-"

    // order id
    document.getElementById("order-id").innerText = Math.floor(Math.random() * 100000)
})