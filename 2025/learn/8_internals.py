class Countdown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1
    
def main() -> None:
    countdown = Countdown(5)
    for number in countdown:
        print(number)

if __name__ == "__main__":
    main()