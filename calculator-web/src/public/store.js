const items = document.querySelectorAll('#items-container > div');
let pendingItemIndex = null;

// Attach click handlers to each Update button
items.forEach((item, index) => {
    const btn = item.querySelector('button');

    btn.addEventListener('click', () => {
        pendingItemIndex = index; // 0 = first item, 1 = second item
        document.getElementById('popup').classList.remove('hidden');
    });
});

// Confirm button
document.getElementById('confirm-btn').addEventListener('click', () => {
    const item = items[pendingItemIndex];
    const price = item.querySelector('input').value;

    console.log("Updated price for item", pendingItemIndex + 1, "=", price);

    document.getElementById('popup').classList.add('hidden');
});

// Cancel button
document.getElementById('cancel-btn').addEventListener('click', () => {
    document.getElementById('popup').classList.add('hidden');
});
