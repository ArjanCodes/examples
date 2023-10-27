"use strict";

function HelpState(layer) {
    powerupjs.GameObjectList.call(this, layer);

    // the background
    var background = new powerupjs.SpriteGameObject(sprites.background_help);
    this.add(background);

    // add a back button
    this.backButton = new powerupjs.Button(sprites.button_back, 100);
    this.backButton.position = new powerupjs.Vector2(415, 720);
    this.add(this.backButton);
}

HelpState.prototype = Object.create(powerupjs.GameObjectList.prototype);

HelpState.prototype.handleInput = function (delta) {
    powerupjs.GameObjectList.prototype.handleInput.call(this, delta);
    if (this.backButton.pressed)
        powerupjs.GameStateManager.switchTo(ID.game_state_title);
};