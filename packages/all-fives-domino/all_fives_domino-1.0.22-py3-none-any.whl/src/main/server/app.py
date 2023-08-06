from flask import Flask, send_from_directory

from src.main.game.Game import Game, GameStatus
from src.main.game.Brain import AllFivesGreedyBrain, PlayerBrain

app = Flask(__name__)

player_brain = PlayerBrain()

game = Game(AllFivesGreedyBrain(), player_brain, interactive=True)


@app.route("/")
def get_page():
    return send_from_directory("static", "index.html")


@app.route("/status")
def get_status():
    return game.json()


@app.route("/start")
async def start_game():
    global game

    if game.status == GameStatus.RUNNING:
        game.status = GameStatus.INTERRUPTED

    game = Game(AllFivesGreedyBrain(), player_brain, interactive=True)
    game.run()
    return "OK"


@app.route("/play/<option>")
def player_decision(option: str):
    player_brain.decision = int(option)
    return "OK"
