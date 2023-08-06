class Number:
    def __init__(self, number = 0):
        self.value: int = number

    def value(self):
        return self.value

    def previous(self):
        return self.value - 1

    def next(self):
        return self.value + 1

    def neighbors(self):
        return self.previous(), self.next()

    def is_positive(self):
        return self.value > 0

    def is_even(self):
        return self.value % 2 == 0
