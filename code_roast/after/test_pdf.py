import unittest

from scrape.pdf import compute_filtered_tokens


class TestPdfScraper(unittest.TestCase):
    def test_filtered_tokens_empty(self):
        self.assertEqual(len(compute_filtered_tokens([])), 0)

    def test_filtered_tokens_stop(self):
        tokens = ["please like and subscribe"]
        filtered_tokens = compute_filtered_tokens(tokens)
        print(tokens)
        print(filtered_tokens)
        self.assertEqual(filtered_tokens, {"please", "like", "subscribe"})


if __name__ == "__main__":
    unittest.main()
