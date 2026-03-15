document.getElementById("login-btn").addEventListener("click", () => {
    const fields = document.querySelectorAll(".dynamic-field");

    const username = fields[0].value;
    const password = fields[1].value;

    // No validation required
    window.location.href = "store.html";
});
