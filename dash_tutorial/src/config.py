from dataclasses import dataclass
from typing import Any, Optional, cast

import omegaconf as oc

SETTINGS_PATH = "./config/settings.yaml"


@dataclass
class SimpleComponent:
    id: str = oc.MISSING
    class_name: Optional[str] = None
    title: Optional[str] = None


@dataclass
class Components:
    year_dropdown: SimpleComponent = SimpleComponent()
    year_button: SimpleComponent = SimpleComponent()
    month_dropdown: SimpleComponent = SimpleComponent()
    month_button: SimpleComponent = SimpleComponent()
    category_dropdown: SimpleComponent = SimpleComponent()
    category_button: SimpleComponent = SimpleComponent()
    pie_chart: SimpleComponent = SimpleComponent()
    bar_chart: SimpleComponent = SimpleComponent()
    records: SimpleComponent = SimpleComponent()
    year_button_clicks: SimpleComponent = SimpleComponent()
    month_button_clicks: SimpleComponent = SimpleComponent()
    category_button_clicks: SimpleComponent = SimpleComponent()


@dataclass
class App:
    title: str = oc.MISSING
    html_class_name: str = oc.MISSING
    components: Components = Components()


@dataclass
class Columns:
    date: str = oc.MISSING
    amount: str = oc.MISSING
    category: str = oc.MISSING
    year: str = oc.MISSING
    month: str = oc.MISSING


@dataclass
class Data:
    path: str = oc.MISSING
    columns: Columns = Columns()


@dataclass
class Paths:
    transactions: str = oc.MISSING


@dataclass
class Dates:
    year_format: str = oc.MISSING
    month_format: str = oc.MISSING
    day_format: str = oc.MISSING
    date_format: str = oc.MISSING


@dataclass
class Text:
    year_dropdown_title: str = oc.MISSING
    month_dropdown_title: str = oc.MISSING
    category_dropdown_title: str = oc.MISSING
    button: str = oc.MISSING


@dataclass
class SettingsSchema:
    debug: bool = oc.MISSING
    app: App = App()
    data: Data = Data()
    components: Components = Components()
    dates: Dates = Dates()
    text: Text = Text()
    _DEFAULTS: Any = None


def load_settings() -> SettingsSchema:
    schema: SettingsSchema = oc.OmegaConf.structured(SettingsSchema)
    settings = oc.OmegaConf.merge(schema, oc.OmegaConf.load(SETTINGS_PATH))
    oc.OmegaConf.resolve(settings)
    return cast(SettingsSchema, settings)


SETTINGS = load_settings()
