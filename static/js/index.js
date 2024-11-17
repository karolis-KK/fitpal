const menu_btn = document.getElementById('menu-btn');

menu_btn.addEventListener('click', () => {
    document.getElementById('menu').className = "bg-black/40 h-screen absolute inset-0 z-20 flex items-center justify-end";
});

document.getElementById("close-menu").addEventListener("click", () => {
    document.getElementById("menu").className = "bg-black/40 h-screen absolute inset-0 z-20 hidden items-center justify-end"
})