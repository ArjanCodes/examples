import gc


class Link:
    def __init__(self, next: "Link | None" = None, prev: "Link | None" = None):
        self.next = next
        if next is not None:
            next.prev = self
        self.prev = prev
        if prev is not None:
            prev.next = self
        self.surprise: "Link | None" = None


def make_chain(depth: int) -> Link:
    head = Link()
    for _i in range(depth):
        head = Link(head, head.prev)
    return head


G1_THRESHOLD = 4000  # Change these to see the effect
G2_THRESHOLD = 6000  # Change these to see the effect
G3_THRESHOLD = 0

gc.set_threshold(G1_THRESHOLD, G2_THRESHOLD, G3_THRESHOLD)

M = 10_000
N = 5_000


def main() -> None:
    chain = make_chain(M)
    count = M

    next_count = 1_000_000
    while True:
        newhead = make_chain(N)
        newhead.prev = chain  # Unpurpose to create a circular reference
        count += N

        if count >= next_count:
            (g1, g2, g3) = gc.get_count()
            print(f"Current collections: {g1}, {g2}, {g3}")
            print(gc.get_stats())

            next_count += 1_000_000


if __name__ == "__main__":
    main()
