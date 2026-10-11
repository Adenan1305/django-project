async function loadRewards() {
    const section = document.getElementById("rewards-section");
    if (!section) return;

    const status = document.getElementById("rewards-status");
    const points = document.getElementById("rewards-points-value");

    try {
        const response = await fetch("/api/rewards/", {
            credentials: "same-origin"
        });
        const contentType = response.headers.get("content-type") || "";
        if (!response.ok || !contentType.includes("application/json")) {
            throw new Error("Sign in to view and redeem your points.");
        }

        const data = await response.json();
        if (!Number.isInteger(data.points) || !Array.isArray(data.rewards)) {
            throw new Error("Unable to load rewards.");
        }

        if (points) points.innerText = data.points;
        data.rewards.forEach(reward => {
            const button = document.querySelector(
                `[data-redeem-product="${reward.product_id}"]`
            );
            if (!button) return;
            button.dataset.pointsCost = reward.points;
            button.disabled = data.points < reward.points;
            button.title = button.disabled
                ? `You need ${reward.points} points to redeem this item.`
                : "";
        });
    } catch (error) {
        if (status) status.innerText = error.message;
        else console.error("Cannot load rewards:", error);
    }
}

function redeemReward(productId) {
    const rewardProductId = Number(productId);
    if (![9, 11].includes(rewardProductId)) {
        alert("This item cannot be redeemed.");
        return;
    }

    const product = products.find(item => item.id === rewardProductId);
    if (!product) {
        alert("This reward is currently unavailable.");
        return;
    }

    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const key = `reward-${rewardProductId}`;
    if (cart.some(item => item.key === key)) {
        alert("รายการนี้อยู่ในตะกร้าแล้วครับ");
        return;
    }

    cart.push({
        ...product,
        qty: 1,
        price: 0,
        noodle: "",
        egg: false,
        reward: true,
        rewardPoints: 300,
        key
    });
    localStorage.setItem("cart", JSON.stringify(cart));

    if (typeof updateCartBadge === "function") updateCartBadge();
    if (typeof renderCart === "function") renderCart();
    if (typeof updateSummary === "function") updateSummary();

    alert(`${product.name} ถูกเพิ่มลงตะกร้าแล้วครับ`);
}

document.addEventListener("DOMContentLoaded", () => {
    const section = document.getElementById("rewards-section");
    if (section && window.location.hash === "#rewards-section") {
        section.open = true;
        requestAnimationFrame(() => {
            section.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    }
    loadRewards();
});
