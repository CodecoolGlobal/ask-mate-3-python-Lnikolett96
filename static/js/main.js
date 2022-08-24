function accept() {
    let button = document.querySelector("#accept")
    if (button) {
        let parent = button.parentNode;
        let newElement = document.createElement('i')
        newElement.className = "fa-solid fa-badge-check";
        parent.insertBefore(newElement, button);
        parent.removeChild(button);
        }
}
