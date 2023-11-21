class BirthRule:
    @staticmethod
    def apply(cell, live_neighbors):
        if cell == 0 and live_neighbors == 3:
            return 1
        return None


class LonelyDeathRule:
    @staticmethod
    def apply(cell, live_neighbors):
        if cell == 1 and live_neighbors < 2:
            return 0
        return None


class StayAliveRule:
    @staticmethod
    def apply(cell, live_neighbors):
        if cell == 1 and 2 <= live_neighbors <= 3:
            return 1
        return None


class OverPopulateRule:
    @staticmethod
    def apply(cell, live_neighbors):
        if cell == 1 and live_neighbors > 3:
            return 0
        return None
