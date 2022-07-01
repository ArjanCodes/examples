from dataclasses import dataclass
from typing import cast

import omegaconf as oc

SETTINGS_PATH = "./config/settings.yaml"


@dataclass
class SettingsSchema:
    data_path: str = oc.MISSING
    debug: bool = False
    locale: str = "en"


def load_settings() -> SettingsSchema:
    schema: SettingsSchema = oc.OmegaConf.structured(SettingsSchema)
    settings = oc.OmegaConf.merge(schema, oc.OmegaConf.load(SETTINGS_PATH))
    oc.OmegaConf.resolve(settings)
    return cast(SettingsSchema, settings)


SETTINGS = load_settings()
