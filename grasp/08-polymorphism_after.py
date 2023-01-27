from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Converter:
    """Apply a unit conversion according to the specified formula."""

    formula: Formula

    def convert(self, input_value: float) -> None:
        self.formula.apply_conversion(input_value)


class Formula(ABC):
    """Interface for unit transformations."""

    @abstractmethod
    def apply_conversion(self, input_value: float) -> None:
        raise NotImplementedError("Subclass should implement calculate method.")


class InchesToCentimeters(Formula):
    """Inch to centimeter transformation."""

    def apply_conversion(self, input_value: float) -> None:
        """Print input value transformed from inch to cm."""
        output_value = input_value * 2.54
        print(f"{input_value} inches becomes {output_value:.4f} centimeters.")


class MilesToKilometers(Formula):
    """Miles to kilometer transformation."""

    def apply_conversion(self, input_value: float):
        """Print input value transformed from miles to km."""
        output_value = input_value * 1.609
        print(f"{input_value} miles becomes {output_value:.4f} kilometers.")


class PoundsToKilograms(Formula):
    """Pounds to kilograms transformation."""

    def apply_conversion(self, input_value: float):
        """Print input value transformed pounds to kg."""
        output_value = input_value / 2.205
        print(f"{input_value} pounds becomes {output_value:.4f} kilograms.")


def main() -> None:
    input_value = 40

    inches_to_cm_converter = Converter(InchesToCentimeters())
    inches_to_cm_converter.convert(input_value)

    miles_to_km_converter = Converter(MilesToKilometers())
    miles_to_km_converter.convert(input_value)

    pounds_to_kg_converter = Converter(PoundsToKilograms())
    pounds_to_kg_converter.convert(input_value)


if __name__ == "__main__":
    main()
