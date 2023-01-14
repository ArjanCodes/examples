from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class ConversionType(Enum):
    """Types of unit conversion."""

    INCHES_TO_CM = auto()
    MILES_TO_KM = auto()
    POUNDS_TO_KG = auto()


@dataclass
class Converter:
    type: ConversionType

    def convert(self, input_value: float):
        """Converts the input value into an output depending on specified conversion type."""
        if self.type == ConversionType.INCHES_TO_CM:
            output_value = input_value * 2.54
            print(f"{input_value} inches becomes {output_value:.4f} centimeters.")

        elif self.type == ConversionType.MILES_TO_KM:
            output_value = input_value * 1.609
            print(f"{input_value} miles becomes {output_value:.4f} kilometers.")

        elif self.type == ConversionType.POUNDS_TO_KG:
            output_value = input_value / 2.205
            print(f"{input_value} pounds becomes {output_value:.4f} kilograms.")


def main():
    input_value = 1

    inches_to_cm_conv = Converter(type=ConversionType.INCHES_TO_CM)
    inches_to_cm_conv.convert(input_value)

    miles_to_km = Converter(type=ConversionType.MILES_TO_KM)
    miles_to_km.convert(input_value)

    pounds_to_kg = Converter(type=ConversionType.POUNDS_TO_KG)
    pounds_to_kg.convert(input_value)


if __name__ == "__main__":
    main()
