from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Converter:
    formula: Formula

    def convert(self):
        self.formula.calculate()


@dataclass
class Formula(ABC):
    @abstractmethod
    def calculate(self):
        raise NotImplementedError("Subclass should implement calculate method.")


@dataclass
class InchesToCentimeters(Formula):
    input_value: float

    def calculate(self):
        output_value = self.input_value * 2.54
        print(f"{self.input_value} inches becomes {output_value:.4f} centimeters.")


@dataclass
class MilesToKilometers(Formula):
    input_value: float

    def calculate(self):
        output_value = self.input_value * 1.609
        print(f"{self.input_value} miles becomes {output_value:.4f} kilometers.")


@dataclass
class PoundsToKilograms(Formula):
    input_value: float

    def calculate(self):
        output_value = self.input_value / 2.205
        print(f"{self.input_value} pounds becomes {output_value:.4f} kilograms.")


def main():
    input_value = 40

    inches_to_cm_conv = Converter(InchesToCentimeters(input_value))
    inches_to_cm_conv.convert()

    pounds_to_kilo = Converter(MilesToKilometers(input_value))
    pounds_to_kilo.convert()

    pounds_to_kilo = Converter(PoundsToKilograms(input_value))
    pounds_to_kilo.convert()


if __name__ == "__main__":
    main()
