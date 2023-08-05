let state;
let previousState;

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

setTimeout(refreshState, 1000)
