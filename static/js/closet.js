const add_clothes = document.querySelectorAll("#add_clothes");
const closeAddButton = document.getElementById("close-add");
const editButtons = document.querySelectorAll(".edit-button");
const editPopup = document.getElementById("edit-popup");
const editForm = document.getElementById("edit-form");
const editClothingTextInput = document.getElementById("edit_clothing_text");
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

// Show Add Item Popup
add_clothes.forEach(button => {
    button.addEventListener("click", () => {
        flashPopup.classList.remove("hidden");
        flashPopup.classList.add("flex");
    });
});

// Close Add Item Popup
closeAddButton.addEventListener("click", () => {
    flashPopup.classList.remove("flex");
    flashPopup.classList.add("hidden");
});

// Show Edit Item Popup
editButtons.forEach(button => {
    button.addEventListener("click", (event) => {
        const itemId = button.getAttribute("data-item-id");
        const currentText = button.getAttribute("data-current-text");

        // Set the form action to the edit route
        editForm.action = `/edit-clothing/${itemId}`;
        // Populate the input with the current text
        editClothingTextInput.value = currentText;

        // Show the edit popup
        editPopup.classList.remove("hidden");
        editPopup.classList.add("flex");
    });
});

// Close Edit Item Popup
closeEditButton.addEventListener("click", () => {
    editPopup.classList.remove("flex");
    editPopup.classList.add("hidden");
});