const filterItems = document.querySelectorAll(".filters ul li");

filterItems.forEach((item) => {
    item.onclick = () => {
        filterItems.forEach((el) => el.classList.remove("active"));
        item.classList.add("active");
    };
});