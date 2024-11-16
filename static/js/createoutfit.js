document.getElementById("top").addEventListener("click", () => {
    document.getElementById("top-popup").classList.remove("hidden");
    document.getElementById("top-popup").classList.add("flex");
})

document.getElementById("close-popup-top").addEventListener("click", () => {
    document.getElementById("top-popup").classList.remove("flex");
    document.getElementById("top-popup").classList.add("hidden");
})

document.getElementById("bottom").addEventListener("click", () => {
    document.getElementById("bottom-popup").classList.remove("hidden");
    document.getElementById("bottom-popup").classList.add("flex");
})

document.getElementById("close-popup-bottom").addEventListener("click", () => {
    document.getElementById("bottom-popup").classList.remove("flex");
    document.getElementById("bottom-popup").classList.add("hidden");
})

document.getElementById("middle").addEventListener("click", () => {
    document.getElementById("middle-popup").classList.remove("hidden");
    document.getElementById("middle-popup").classList.add("flex");
})

document.getElementById("close-popup-middle").addEventListener("click", () => {
    document.getElementById("middle-popup").classList.remove("flex");
    document.getElementById("middle-popup").classList.add("hidden");
})

document.querySelectorAll(".selected_item_top").forEach(element => {
    element.addEventListener("click", () => {
        document.getElementById("top-popup").classList.remove("flex");
        document.getElementById("top-popup").classList.add("hidden");

        document.querySelectorAll(".hr").forEach(element => {
            element.classList.add("hidden");
        })

        const image_1 = element.querySelector(".top_inner").src;

        document.getElementById("top").innerHTML = `<img src="${image_1}" alt="Selected Top" class="w-full h-full object-contain">`;
    });
});

document.querySelectorAll(".selected_item_middle").forEach(element => {
    element.addEventListener("click", () => {
        document.getElementById("middle-popup").classList.remove("flex");
        document.getElementById("middle-popup").classList.add("hidden");
    
        document.querySelectorAll(".hr").forEach(element => {
            element.classList.add("hidden");
        })

        const image_2 = element.querySelector(".middle_inner").src;

        document.getElementById("middle").innerHTML = `<img src="${image_2}" alt="Selected Middle" class="w-full h-full object-contain -mt-12">`;
        document.getElementById("middle").classList.remove("my-2");
    })
})

document.querySelectorAll(".selected_item_bottom").forEach(element => {
    element.addEventListener("click", () => {
        document.getElementById("bottom-popup").classList.remove("flex");
        document.getElementById("bottom-popup").classList.add("hidden");

        document.querySelectorAll(".hr").forEach(element => {
            element.classList.add("hidden");
        })
    
        const image_3 = element.querySelector(".bottom_inner").src;

        document.getElementById("bottom").innerHTML = `<img src="${image_3}" alt="Selected Bottom" class="w-full h-full object-contain -mt-12">`;
    })
})

document.getElementById("save").addEventListener("click", () => {
    document.getElementById("save-popup").classList.remove("hidden");
    document.getElementById("save-popup").classList.add("flex");
});

document.getElementById("close-save").addEventListener("click", () => {
    document.getElementById("save-popup").classList.remove("flex");
    document.getElementById("save-popup").classList.add("hidden");
})

document.getElementById("save-outfit").addEventListener("click", () => {
    const outfitName = document.getElementById("outfit_name").value;
    const topImage = document.getElementById("top").querySelector("img")?.src || '';
    const middleImage = document.getElementById("middle").querySelector("img")?.src || '';
    const bottomImage = document.getElementById("bottom").querySelector("img")?.src || '';

    const outfitData = {
        name: outfitName,
        top: topImage,
        middle: middleImage,
        bottom: bottomImage
    };

    fetch('/save-outfit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(outfitData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Outfit saved successfully!');
            document.getElementById("save-popup").classList.add("hidden");
        } else {
            console.log('Failed to save outfit.');
        }
    })
    .catch(error => console.error('Error:', error));
});