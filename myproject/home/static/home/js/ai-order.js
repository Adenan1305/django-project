// ==========================================
// AI ORDER SYSTEM
// ==========================================


// ==========================================
// 1. AI ORDER RULES
// ==========================================

const AI_ORDER_RULES = {

    // --------------------------------------
    // NOODLE TYPES
    // --------------------------------------

    noodle: {

        types: {
            "เส้นเล็ก": "Thin",
            "เล็ก": "Thin",

            "เส้นใหญ่": "Wide",
            "ใหญ่": "Wide",

            "บะหมี่": "egg noodles"
        },

        defaultNoodle: "Thin",

        // เมนูก๋วยเตี๋ยวต้องมีคำระบุเมนูชัดเจน
        requireMenuName: true
    },


    // --------------------------------------
    // EGG
    // --------------------------------------

    egg: {

        yes: [
            "เพิ่มไข่",
            "ใส่ไข่",
            "เอาไข่",
            "ไข่เพิ่ม"
        ],

        no: [
            "ไม่ใส่ไข่",
            "ไม่เอาไข่",
            "ไม่ต้องใส่ไข่"
        ],

        default: false
    }

};


// ==========================================
// 2. MENU RULES
// ==========================================

const AI_MENU_RULES = {

    // --------------------------------------
    // ID 1
    // --------------------------------------

    1: {

        name: "Tom Yum Noodles + rice",

        keywords: [
            "ต้มยำพร้อมข้าว",
            "ก๋วยเตี๋ยวต้มยำพร้อมข้าว",
            "ต้มยำ + ข้าว"
        ],

        ambiguous: [
            "ต้มยำ"
        ],

        type: "both"
    },


    // --------------------------------------
    // ID 2
    // --------------------------------------

    2: {

        name: "Beef offal rice with spicy dipping sauce",

        keywords: [
            "ข้าวเครื่องใน",
            "ข้าวเครื่องในพร้อมน้ำจิ้ม",
            "เครื่องในราดข้าว"
        ],

        ambiguous: [
            "เครื่องใน"
        ],

        type: "rice"
    },


    // --------------------------------------
    // ID 3
    // --------------------------------------

    3: {

        name: "Beef noodles + Chicken noodles",

        keywords: [
            "ก๋วยเตี๋ยวเนื้อกับก๋วยเตี๋ยวไก่",
            "ก๋วยเตี๋ยวเนื้อและก๋วยเตี๋ยวไก่",
            "ก๋วยเตี๋ยวเนื้อ + ก๋วยเตี๋ยวไก่"
        ],

        type: "noodle"
    },


    // --------------------------------------
    // ID 4
    // --------------------------------------

    4: {

        name: "Tom Yum Noodles",

        keywords: [
            "ก๋วยเตี๋ยวต้มยำ",
            "ต้มยำเส้น",
            "tom yum noodles"
        ],

        ambiguous: [
            "ต้มยำ"
        ],

        type: "noodle"
    },


    // --------------------------------------
    // ID 5
    // --------------------------------------

    5: {

        name: "Chicken noodles",

        keywords: [
            "ก๋วยเตี๋ยวไก่",
            "chicken noodles"
        ],

        ambiguous: [
            "ไก่"
        ],

        type: "noodle"
    },


    // --------------------------------------
    // ID 6
    // --------------------------------------

    6: {

        name: "Beef noodles",

        keywords: [
            "ก๋วยเตี๋ยวเนื้อ",
            "beef noodles"
        ],

        ambiguous: [
            "เนื้อ"
        ],

        type: "noodle"
    },


    // --------------------------------------
    // ID 7
    // --------------------------------------

    7: {

        name: "Bottled Water",

        keywords: [
            "น้ำเปล่า",
            "น้ำดื่ม",
            "bottled water"
        ],

        ambiguous: [
            "น้ำ"
        ],

        type: "drink"
    },


    // --------------------------------------
    // ID 8
    // --------------------------------------

    8: {

        name: "Soft Drinks",

        keywords: [
            "น้ำอัดลม",
            "soft drink"
        ],

        type: "drink"
    },


    // --------------------------------------
    // ID 9
    // --------------------------------------

    9: {

        name: "Ice cream",

        keywords: [
            "ไอศกรีม",
            "ไอติม",
            "ice cream"
        ],

        type: "drink"
    },


    // --------------------------------------
    // ID 10
    // --------------------------------------

    10: {

        name: "Beef intestines with spicy dipping sauce",

        keywords: [
            "เครื่องในจิ้ม",
            "ไส้พร้อมน้ำจิ้ม",
            "ไส้จิ้ม"
        ],

        ambiguous: [
            "เครื่องใน",
            "ไส้"
        ],

        type: "snacks"
    },


    // --------------------------------------
    // ID 11
    // --------------------------------------

    11: {

        name: "Fried meatballs",

        keywords: [
            "ลูกชิ้นทอด",
            "fried meatballs"
        ],

        ambiguous: [
            "ลูกชิ้น"
        ],

        type: "snacks"
    },


    // --------------------------------------
    // ID 12
    // --------------------------------------

    12: {

        name: "Fried dumplings",

        keywords: [
            "เกี๊ยวทอด",
            "fried dumplings"
        ],

        ambiguous: [
            "เกี๊ยว"
        ],

        type: "snacks"
    }

};


// ==========================================
// 3. THAI NUMBER → ARABIC NUMBER
// ==========================================

function thaiNumberToArabic(text) {

    const map = {

        "๐": "0",
        "๑": "1",
        "๒": "2",
        "๓": "3",
        "๔": "4",
        "๕": "5",
        "๖": "6",
        "๗": "7",
        "๘": "8",
        "๙": "9"

    };

    return text.replace(/[๐-๙]/g, char => map[char]);
}


// ==========================================
// 4. EXTRACT QUANTITY
// ==========================================

function extractQuantity(text) {

    text = thaiNumberToArabic(text);

    // ตัวเลข เช่น 2, 3, 10
    const number = text.match(/\d+/);

    if (number) {

        const quantity = parseInt(number[0]);

        if (quantity > 0) {
            return quantity;
        }
    }


    // คำอ่านจำนวน
    const numbers = {

        "หนึ่ง": 1,
        "สอง": 2,
        "สาม": 3,
        "สี่": 4,
        "ห้า": 5,
        "หก": 6,
        "เจ็ด": 7,
        "แปด": 8,
        "เก้า": 9,
        "สิบ": 10

    };


    for (const word in numbers) {

        if (text.includes(word)) {

            return numbers[word];

        }

    }


    // ถ้าไม่ระบุจำนวน
    return 1;
}


// ==========================================
// 5. FIND NOODLE TYPE
// ==========================================

function findNoodleType(text) {

    const normalized = text.toLowerCase();

    const noodleTypes =
        AI_ORDER_RULES.noodle.types;


    for (const keyword in noodleTypes) {

        if (normalized.includes(keyword)) {

            return noodleTypes[keyword];

        }

    }


    // ไม่ระบุเส้น → Thin
    return AI_ORDER_RULES.noodle.defaultNoodle;
}


// ==========================================
// 6. FIND EGG
// ==========================================

function findEgg(text) {

    const normalized = text.toLowerCase();


    // ต้องเช็ค "ไม่..." ก่อน
    // เพื่อไม่ให้ "ไม่ใส่ไข่"
    // ถูกอ่านเป็นใส่ไข่

    for (const keyword of AI_ORDER_RULES.egg.no) {

        if (normalized.includes(keyword)) {

            return false;

        }

    }


    for (const keyword of AI_ORDER_RULES.egg.yes) {

        if (normalized.includes(keyword)) {

            return true;

        }

    }


    return AI_ORDER_RULES.egg.default;
}


// ==========================================
// 7. FIND EXACT MENU
// ==========================================

function findExactMenu(text) {

    const normalized = text
        .toLowerCase()
        .trim();


    const matches = [];


    for (const id in AI_MENU_RULES) {

        const rule = AI_MENU_RULES[id];


        for (const keyword of rule.keywords) {

            if (
                normalized.includes(
                    keyword.toLowerCase()
                )
            ) {

                matches.push({
                    id: parseInt(id),
                    keyword: keyword
                });

            }

        }

    }


    // ไม่มีเมนู
    if (matches.length === 0) {

        return null;

    }


    // เลือก keyword ที่ยาวที่สุด
    matches.sort(
        (a, b) =>
            b.keyword.length -
            a.keyword.length
    );


    const selected = matches[0];


    const product = products.find(
        product =>
            product.id === selected.id
    );


    if (!product) {

        return null;

    }


    return product;
}


// ==========================================
// 8. CHECK AMBIGUOUS MENU
// ==========================================

function checkAmbiguous(text) {

    const normalized =
        text.toLowerCase().trim();


    // -------------------------------
    // ไก่
    // -------------------------------

    if (
        normalized.includes("ไก่") &&
        !normalized.includes("ก๋วยเตี๋ยวไก่")
    ) {

        return {
            required: true,

            message:
                "ต้องการก๋วยเตี๋ยวไก่ใช่ไหมครับ?"
        };

    }


    // -------------------------------
    // เนื้อ
    // -------------------------------

    if (
        normalized.includes("เนื้อ") &&
        !normalized.includes("ก๋วยเตี๋ยวเนื้อ") &&
        !normalized.includes("ข้าวเครื่องใน")
    ) {

        return {
            required: true,

            message:
                "ต้องการก๋วยเตี๋ยวเนื้อใช่ไหมครับ?"
        };

    }


    // -------------------------------
    // ต้มยำ
    // -------------------------------

    if (
        normalized.includes("ต้มยำ") &&
        !normalized.includes("ก๋วยเตี๋ยวต้มยำ") &&
        !normalized.includes("ต้มยำเส้น") &&
        !normalized.includes("ต้มยำพร้อมข้าว")
    ) {

        return {
            required: true,

            message:
                "ต้องการก๋วยเตี๋ยวต้มยำ หรือ ต้มยำพร้อมข้าวครับ?"
        };

    }


    // -------------------------------
    // เครื่องใน
    // -------------------------------

    if (
        normalized.includes("เครื่องใน") &&
        !normalized.includes("ข้าวเครื่องใน") &&
        !normalized.includes("เครื่องในจิ้ม")
    ) {

        return {
            required: true,

            message:
                "ต้องการข้าวเครื่องใน หรือ เครื่องในพร้อมน้ำจิ้มครับ?"
        };

    }


    // -------------------------------
    // น้ำ
    // -------------------------------

    if (
        normalized.includes("น้ำ") &&
        !normalized.includes("น้ำเปล่า") &&
        !normalized.includes("น้ำดื่ม") &&
        !normalized.includes("น้ำอัดลม")
    ) {

        return {
            required: true,

            message:
                "ต้องการน้ำเปล่าหรือน้ำอัดลมครับ?"
        };

    }


    // -------------------------------
    // ลูกชิ้น
    // -------------------------------

    if (
        normalized.includes("ลูกชิ้น") &&
        !normalized.includes("ลูกชิ้นทอด")
    ) {

        return {
            required: true,

            message:
                "ต้องการลูกชิ้นทอดใช่ไหมครับ?"
        };

    }


    // -------------------------------
    // เกี๊ยว
    // -------------------------------

    if (
        normalized.includes("เกี๊ยว") &&
        !normalized.includes("เกี๊ยวทอด")
    ) {

        return {
            required: true,

            message:
                "ต้องการเกี๊ยวทอดใช่ไหมครับ?"
        };

    }


    return {
        required: false
    };
}


// ==========================================
// 9. PARSE ONE ORDER
// ==========================================

function parseSingleAIOrder(part) {

    const text =
        thaiNumberToArabic(
            part.toLowerCase().trim()
        );


    // --------------------------------------
    // ตรวจคำกำกวมก่อน
    // --------------------------------------

    const ambiguity =
        checkAmbiguous(text);


    if (ambiguity.required) {

        return {
            success: false,

            clarification:
                ambiguity.message
        };

    }


    // --------------------------------------
    // หาเมนู
    // --------------------------------------

    const product =
        findExactMenu(text);


    if (!product) {

        return {
            success: false,

            clarification:
                "ไม่พบเมนูที่ตรงกับคำสั่งครับ กรุณาระบุชื่อเมนูให้ชัดเจน"
        };

    }


    // --------------------------------------
    // จำนวน
    // --------------------------------------

    const quantity =
        extractQuantity(text);


    // --------------------------------------
    // เส้น
    // --------------------------------------

    let noodle = "";

    if (
        product.type === "noodle" ||
        product.type === "both"
    ) {

        noodle =
            findNoodleType(text);

    }


    // --------------------------------------
    // ไข่
    // --------------------------------------

    const egg =
        findEgg(text);


    return {

        success: true,

        item: {

            product_id: product.id,

            quantity: quantity,

            noodle: noodle,

            egg: egg

        }

    };

}


// ==========================================
// 10. SPLIT ORDER
// ==========================================

function splitAIOrder(message) {

    let text =
        thaiNumberToArabic(
            message.toLowerCase()
        );


    /*
        เราจะยังไม่ split "กับ" / "และ"
        แบบง่าย ๆ เพราะอาจทำให้เมนู ID 3
        ถูกแยกผิด

        ตัวอย่าง:

        ก๋วยเตี๋ยวเนื้อกับก๋วยเตี๋ยวไก่
        ↓
        ต้องถือเป็นเมนูเดียว
    */


    // กรณีเมนู ID 3 ก่อน
    const combinedMenu =
        findExactMenu(text);


    if (
        combinedMenu &&
        combinedMenu.id === 3
    ) {

        return [text];

    }


    // แยกรายการทั่วไป
    return text
        .split(/\s+(?:กับ|และ)\s+|,/)
        .map(part => part.trim())
        .filter(Boolean);

}


// ==========================================
// 11. PARSE AI ORDER
// ==========================================

function parseAIOrder(message) {

    const parts =
        splitAIOrder(message);


    const items = [];


    for (const part of parts) {

        const result =
            parseSingleAIOrder(part);


        // ------------------------------
        // ต้องถามกลับ
        // ------------------------------

        if (!result.success) {

            return {

                success: false,

                items: [],

                clarification:
                    result.clarification

            };

        }


        items.push(result.item);

    }


    return {

        success: true,

        items: items

    };

}


// ==========================================
// 12. VALIDATE AI ITEMS
// ==========================================

function validateAIItems(items) {

    const validItems = [];


    for (const item of items) {

        const product =
            products.find(
                product =>
                    product.id ===
                    item.product_id
            );


        // ไม่มี Product ID
        if (!product) {

            console.warn(
                "Invalid AI product ID:",
                item.product_id
            );

            continue;

        }


        // จำนวนผิด
        if (
            !Number.isInteger(
                item.quantity
            ) ||
            item.quantity < 1
        ) {

            continue;

        }


        // ตรวจ noodle
        if (
            product.type === "noodle" &&
            !item.noodle
        ) {

            item.noodle =
                AI_ORDER_RULES
                    .noodle
                    .defaultNoodle;

        }


        validItems.push(item);

    }


    return validItems;

}


// ==========================================
// 13. ADD AI ITEMS TO CART
// ==========================================

function addAIItemsToCart(items) {

    let cart =
        JSON.parse(
            localStorage.getItem("cart")
        ) || [];


    items.forEach(orderItem => {

        const product =
            products.find(
                product =>
                    product.id ===
                    orderItem.product_id
            );


        if (!product) {
            return;
        }


        const noodle =
            orderItem.noodle || "";


        const egg =
            orderItem.egg || false;


        const key =
            `${product.id}-${noodle}-${egg}`;


        const existing =
            cart.find(
                item =>
                    item.key === key
            );


        if (existing) {

            existing.qty +=
                orderItem.quantity;

        } else {

            cart.push({

                ...product,

                qty:
                    orderItem.quantity,

                noodle:
                    noodle,

                egg:
                    egg,

                key:
                    key

            });

        }

    });


    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );


    // --------------------------------------
    // Update Cart
    // --------------------------------------

    if (
        typeof updateCartBadge ===
        "function"
    ) {

        updateCartBadge();

    }


    if (
        typeof renderCart ===
        "function"
    ) {

        renderCart();

    }


    if (
        typeof updateSummary ===
        "function"
    ) {

        updateSummary();

    }

}


// ==========================================
// 14. MAIN AI ORDER FUNCTION
// ==========================================

function processAIOrder(message) {

    if (
        !message ||
        !message.trim()
    ) {

        return {

            success: false,

            items: [],

            message:
                "กรุณาพิมพ์รายการอาหาร"

        };

    }


    // --------------------------------------
    // Parse
    // --------------------------------------

    const parsed =
        parseAIOrder(message);


    // --------------------------------------
    // ถ้าต้องถามลูกค้า
    // --------------------------------------

    if (!parsed.success) {

        return {

            success: false,

            items: [],

            clarification:
                parsed.clarification,

            message:
                parsed.clarification

        };

    }


    // --------------------------------------
    // Validate
    // --------------------------------------

    const validItems =
        validateAIItems(
            parsed.items
        );


    if (
        validItems.length === 0
    ) {

        return {

            success: false,

            items: [],

            message:
                "ไม่พบรายการอาหารที่ถูกต้อง"

        };

    }


    // --------------------------------------
    // Add Cart
    // --------------------------------------

    addAIItemsToCart(
        validItems
    );


    // --------------------------------------
    // Return Result
    // --------------------------------------

    return {

        success: true,

        items: validItems,

        message:
            "เพิ่มรายการลงตะกร้าเรียบร้อยแล้ว"

    };

}


// ==========================================
// AI ORDER UI
// ==========================================

function getCookie(name) {
    const cookie = document.cookie
        .split("; ")
        .find(item => item.startsWith(`${name}=`));

    return cookie ? cookie.slice(name.length + 1) : "";
}

async function submitAIOrder() {

    const input = document.getElementById("aiOrderInput");
    const result = document.getElementById("aiOrderResult");
    const button = document.getElementById("aiOrderButton");

    if (!input || !result) return;

    const resultClass = result.classList.contains("home-ai-result")
        ? "home-ai-result"
        : "ai-order-result";
    const message = input.value.trim();

    if (!message) {
        result.className = `${resultClass} error`;
        result.innerText = "กรุณาพิมพ์รายการอาหารก่อนครับ";
        return;
    }

    input.value = "";

    const csrfToken = getCookie("csrftoken");
    if (!csrfToken) {
        result.className = `${resultClass} error`;
        result.innerText = "ไม่สามารถเริ่มสั่งอาหารด้วย AI ได้ กรุณารีเฟรชหน้าเว็บ";
        return;
    }

    if (button) {
        button.disabled = true;
        button.innerHTML = `
            <span>AI กำลังคิด...</span>
            <span>⟳</span>
        `;
    }

    result.className = `${resultClass} question`;
    result.innerText = "กำลังวิเคราะห์รายการอาหาร...";

    try {
        const response = await fetch("/api/ai-order/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            credentials: "same-origin",
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!data.success) {
            result.className = `${resultClass} question`;
            result.innerText = "AI: " + (
                data.clarification ||
                data.error ||
                "กรุณาระบุเมนูให้ชัดเจนครับ"
            );
            return;
        }

        if (typeof data.assistant_message === "string" && data.assistant_message.trim()) {
            result.className = `${resultClass} question`;
            result.innerText = data.assistant_message;
            return;
        }

        if (!Array.isArray(data.items)) {
            throw new Error("AI ส่งข้อมูลรายการอาหารไม่ถูกต้อง");
        }

        addAIItemsToCart(data.items.map(item => ({
            product_id: item.product_id,
            quantity: item.quantity,
            noodle: item.noodle,
            egg: item.egg
        })));

        result.className = `${resultClass} success`;
        result.innerText = "เพิ่มรายการลงตะกร้าเรียบร้อยแล้ว ✓";
    } catch (error) {
        console.error("AI ORDER ERROR:", error);
        result.className = `${resultClass} error`;
        result.innerText = "ไม่สามารถเชื่อมต่อ AI ได้ กรุณาลองใหม่ครับ";
    } finally {
        if (button) {
            button.disabled = false;
            button.innerHTML = `
                <span>สั่งอาหาร</span>
                <span>→</span>
            `;
        }
    }
}

// ==========================================
// USE EXAMPLE
// ==========================================

function useAIExample(text) {

    const input =
        document.getElementById(
            "aiOrderInput"
        );

    if (!input) {
        return;
    }

    input.value = text;

    input.focus();

}

// ==========================================
// ENTER KEY
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const input =
            document.getElementById(
                "aiOrderInput"
            );

        if (!input) {
            return;
        }

        input.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Enter"
                ) {

                    submitAIOrder();

                }

            }
        );

    }
);