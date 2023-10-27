"use strict";

function OptionsMenuState(layer) {
    powerupjs.GameObjectList.call(this, layer);

    var background = new powerupjs.SpriteGameObject(sprites.background_options, ID.layer_background);
    this.add(background);

    var onOffLabel = new powerupjs.Label("Arial", "60px", ID.layer_overlays);
    onOffLabel.text = "Hints";
    onOffLabel.position = new powerupjs.Vector2(150, 360);
    onOffLabel.color = powerupjs.Color.darkBlue;
    this.add(onOffLabel);

    this.onOffButton = new OnOffButton(sprites.button_offon, ID.layer_overlays);
    this.onOffButton.position = new powerupjs.Vector2(650, 340);
    this.onOffButton.on = GameSettings.hints;
    this.add(this.onOffButton);

    var musicText = new powerupjs.Label("Arial", "60px", ID.layer_overlays);
    musicText.text = "Music volume";
    musicText.position = new powerupjs.Vector2(150, 490);
    musicText.color = powerupjs.Color.darkBlue;
    this.add(musicText);

    this.musicSlider = new Slider(sprites.slider_bar, sprites.slider_button, ID.layer_overlays);
    this.musicSlider.position = new powerupjs.Vector2(650, 500);
    this.musicSlider.value = sounds.music.volume;
    this.add(this.musicSlider);

    this.backButton = new powerupjs.Button(sprites.button_back, ID.layer_overlays);
    this.backButton.position = new powerupjs.Vector2(415, 720);
    this.add(this.backButton);
}

OptionsMenuState.prototype = Object.create(powerupjs.GameObjectList.prototype);

OptionsMenuState.prototype.handleInput = function (delta) {
    powerupjs.GameObjectList.prototype.handleInput.call(this, delta);
    if (this.backButton.pressed)
        powerupjs.GameStateManager.switchTo(ID.game_state_title);
};

OptionsMenuState.prototype.update = function (delta) {
    powerupjs.GameObjectList.prototype.update.call(this, delta);
    sounds.music.volume = this.musicSlider.value;
    GameSettings.hints = this.onOffButton.on;
};