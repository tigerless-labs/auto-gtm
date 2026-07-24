#!/usr/bin/env python3
"""Shared token-bucket rate limiter for keyless probes.

A single bucket is shared across all keyless Reddit surfaces (RSS, shreddit
listing/comments, arctic) so concurrent probes can't stampede an endpoint —
per-request retry budgets don't bound concurrency, a shared bucket does.
Defaults: 5 requests/second, burst 5. Stdlib only; clock/sleep are injectable
for deterministic tests.
"""
import threading
import time


class TokenBucket:
    def __init__(self, rate=5.0, capacity=5, clock=time.monotonic, sleep=time.sleep):
        self.rate = float(rate)
        self.capacity = float(capacity)
        self._tokens = float(capacity)
        self._clock = clock
        self._sleep = sleep
        self._last = clock()
        self._lock = threading.Lock()

    def _refill_locked(self):
        now = self._clock()
        self._tokens = min(self.capacity, self._tokens + (now - self._last) * self.rate)
        self._last = now

    def try_acquire(self):
        with self._lock:
            self._refill_locked()
            if self._tokens >= 1:
                self._tokens -= 1
                return True
            return False

    def acquire(self):
        while True:
            with self._lock:
                self._refill_locked()
                if self._tokens >= 1:
                    self._tokens -= 1
                    return
                wait = (1 - self._tokens) / self.rate
            self._sleep(wait)


_shared = None
_shared_lock = threading.Lock()


def shared_bucket():
    """Process-wide bucket for keyless Reddit probes (5 req/s, burst 5)."""
    global _shared
    with _shared_lock:
        if _shared is None:
            _shared = TokenBucket(rate=5.0, capacity=5)
        return _shared
