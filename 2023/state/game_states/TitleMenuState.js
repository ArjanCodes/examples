"use strict";

function TitleMenuState(layer) {
    powerupjs.GameObjectList.call(this, layer);

    var background = new powerupjs.SpriteGameObject(sprites.background_title, ID.layer_background);
    this.add(background);

    this.playButton = new powerupjs.Button(sprites.button_play, ID.layer_overlays);
    this.playButton.position = new powerupjs.Vector2(415, 540);
    this.add(this.playButton);

    this.optionsButton = new powerupjs.Button(sprites.button_options, ID.layer_overlays);
    this.optionsButton.position = new powerupjs.Vector2(415, 650);
    this.add(this.optionsButton);

    this.helpButton = new powerupjs.Button(sprites.button_help, ID.layer_overlays);
    this.helpButton.position = new powerupjs.Vector2(415, 760);
    this.add(this.helpButton);
}

TitleMenuState.prototype = Object.create(powerupjs.GameObjectList.prototype);

TitleMenuState.prototype.handleInput = function (delta) {
    powerupjs.GameObjectList.prototype.handleInput.call(this, delta);
    if (this.playButton.pressed)
        powerupjs.GameStateManager.switchTo(ID.game_state_levelselect);
    else if (this.helpButton.pressed)
        powerupjs.GameStateManager.switchTo(ID.game_state_help);
    else if (this.optionsButton.pressed)
        powerupjs.GameStateManager.switchTo(ID.game_state_options);
};