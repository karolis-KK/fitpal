const add_clothes = document.querySelectorAll("#add_clothes");
const closeAddButton = document.getElementById("close-add");
const editButtons = document.querySelectorAll(".edit-button");
const editPopup = document.getElementById("edit-popup");
const editForm = document.getElementById("edit-form");
const editClothingTextInput = document.getElementById("edit_clothing_text");
const editClothingBrandInput = document.getElementById("edit_clothing_brand");
const closeEditButton = document.getElementById("close-edit");
const flashPopup = document.getElementById("flash-popup");
const filtersPopup = document.getElementById("filters-popup");
const closeFiltersButton = document.getElementById("close-filters");

document.getElementById("filters").addEventListener("click", () => {
    filtersPopup.classList.remove("hidden");
    filtersPopup.classList.add("flex");
})

closeFiltersButton.addEventListener("click", () => {
    filtersPopup.classList.add("hidden");
    filtersPopup.classList.remove("flex");
})

add_clothes.forEach(button => {
    button.addEventListener("click", () => {
        flashPopup.classList.remove("hidden");
        flashPopup.classList.add("flex");
    });
});

closeAddButton.addEventListener("click", () => {
    flashPopup.classList.remove("flex");
    flashPopup.classList.add("hidden");
});

editButtons.forEach(button => {
    button.addEventListener("click", (event) => {
        const itemId = button.getAttribute("data-item-id");
        const currentText = button.getAttribute("data-current-text");
        const currentBrand = button.getAttribute("data-current-brand");

        editForm.action = `/edit-clothing/${itemId}`;
        editClothingTextInput.value = currentText;
        editClothingBrandInput.value = currentBrand;
        
        editPopup.classList.remove("hidden");
        editPopup.classList.add("flex");
    });
});

closeEditButton.addEventListener("click", () => {
    editPopup.classList.remove("flex");
    editPopup.classList.add("hidden");
});