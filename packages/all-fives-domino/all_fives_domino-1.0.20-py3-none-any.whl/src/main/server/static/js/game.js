let state;
let previousState;

let selectedPiece = null;
let piecePositions = {};

const refreshState = () => {
    fetch("/status")
        .then(r => r.json())
        .then(newState => {
            previousState = state;
            state = newState;
            render();
        });
}

const startGame = () => {
    fetch("/start");
}

function toggleSelect(event) {
    console.log(event);
    const sides = event.target.dataset.sides.split(",");

    // If this piece was already selected, unselect it
    if (selectedPiece !== null && selectedPiece[0] === sides[0] && selectedPiece[1] === sides[1]) {
        getHandPiece(selectedPiece).classList.remove("selected");
        selectedPiece = null;
        return;
    }

    if (selectedPiece !== null) {
        getHandPiece(selectedPiece).classList.remove("selected");
    }

    selectedPiece = sides;
    getHandPiece(selectedPiece).classList.add("selected");
}

setTimeout(refreshState, 1000)