const list = document.getElementById("list");
let dragSrcEl = null;

function handleDragStart(e) {
    dragSrcEl = this;
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/html", this.innerHTML);
}

function handleDragOver(e) {
    if (e.preventDefault) e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    return false;
}

function handleDrop(e) {
    if (e.stopPropagation) e.stopPropagation();
    if (dragSrcEl !== this) {
        let temp = dragSrcEl.innerHTML;
        dragSrcEl.innerHTML = this.innerHTML;
        this.innerHTML = temp;
        let tempIndex = dragSrcEl.dataset.index;
        dragSrcEl.dataset.index = this.dataset.index;
        this.dataset.index = tempIndex;
    }
    return false;
}

let items = list.querySelectorAll(".item");
items.forEach(function(item) {
    item.addEventListener("dragstart", handleDragStart, false);
    item.addEventListener("dragover", handleDragOver, false);
    item.addEventListener("drop", handleDrop, false);
});

document.getElementById("checkBtn").addEventListener("click", async function() {
    const arranged = Array.from(list.querySelectorAll(".item")).map(div => +div.dataset.index);
    try {
        const response = await fetch("/zadanie2/check_order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ order: arranged })
        });
        const result = await response.json();
        const resultDiv = document.getElementById("result");
        if (result.result === true) {
            resultDiv.textContent = "Правильно! Можно переходить к следующему заданию.";
            resultDiv.style.color = "green";
        } else if (result.result === false) {
            resultDiv.textContent = "Неправильно! Попробуйте еще раз!";
            resultDiv.style.color = "red";
        } else {
            resultDiv.textContent = "Что-то пошло не так :(";
            resultDiv.style.color = "black";
        }
    } catch (err) {
        console.error(err);
        alert("Ошибка связи с сервером.");
    }
});