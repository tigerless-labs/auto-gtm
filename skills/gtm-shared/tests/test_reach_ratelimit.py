import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts" / "reach"))
import ratelimit  # noqa: E402


class TokenBucketTest(unittest.TestCase):
    def _bucket(self, rate=5, cap=5):
        self.now = [0.0]
        slept = []

        def clock():
            return self.now[0]

        def sleep(s):
            slept.append(s)
            self.now[0] += s

        self.slept = slept
        return ratelimit.TokenBucket(rate=rate, capacity=cap, clock=clock, sleep=sleep)

    def test_burst_then_empty(self):
        b = self._bucket()
        self.assertEqual(sum(b.try_acquire() for _ in range(5)), 5)  # burst of 5
        self.assertFalse(b.try_acquire())                            # 6th blocked

    def test_refills_over_time(self):
        b = self._bucket(rate=5, cap=5)
        for _ in range(5):
            b.try_acquire()
        self.assertFalse(b.try_acquire())
        self.now[0] += 1.0  # 1s -> +5 tokens
        self.assertTrue(b.try_acquire())

    def test_acquire_sleeps_until_token(self):
        b = self._bucket(rate=5, cap=5)
        for _ in range(5):
            b.acquire()      # drains burst, no sleep
        self.assertEqual(self.slept, [])
        b.acquire()          # must wait ~0.2s for one token
        self.assertTrue(self.slept and self.slept[0] > 0)

    def test_shared_bucket_is_singleton(self):
        self.assertIs(ratelimit.shared_bucket(), ratelimit.shared_bucket())


if __name__ == "__main__":
    unittest.main()
