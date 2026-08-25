"""Circuit Breaker — prevent cascading failures with state-based protection."""
import time
from datetime import datetime
from typing import Optional, Callable
from app.models import CircuitBreakerState, CircuitState


class CircuitBreaker:
    """Circuit breaker with closed/open/half-open states."""

    def __init__(self, name: str, failure_threshold: int = 5,
                 recovery_timeout: int = 30, half_open_max_calls: int = 3):
        self.state = CircuitBreakerState(
            name=name,
            failure_threshold=failure_threshold,
            recovery_timeout_seconds=recovery_timeout,
            half_open_max_calls=half_open_max_calls
        )

    def can_execute(self) -> bool:
        if self.state.state == CircuitState.CLOSED:
            return True

        if self.state.state == CircuitState.OPEN:
            if self._recovery_timeout_expired():
                self.state.state = CircuitState.HALF_OPEN
                self.state.half_open_calls = 0
                self.state.success_count = 0
                return True
            return False

        if self.state.state == CircuitState.HALF_OPEN:
            return self.state.half_open_calls < self.state.half_open_max_calls

        return False

    def record_success(self):
        if self.state.state == CircuitState.HALF_OPEN:
            self.state.success_count += 1
            if self.state.success_count >= self.state.half_open_max_calls:
                self._close()
        elif self.state.state == CircuitState.CLOSED:
            self.state.failure_count = max(0, self.state.failure_count - 1)

    def record_failure(self):
        self.state.failure_count += 1
        self.state.last_failure_time = datetime.utcnow()

        if self.state.state == CircuitState.HALF_OPEN:
            self._open()
        elif self.state.state == CircuitState.CLOSED:
            if self.state.failure_count >= self.state.failure_threshold:
                self._open()

    def _open(self):
        self.state.state = CircuitState.OPEN
        self.state.last_failure_time = datetime.utcnow()

    def _close(self):
        self.state.state = CircuitState.CLOSED
        self.state.failure_count = 0
        self.state.success_count = 0
        self.state.half_open_calls = 0

    def _recovery_timeout_expired(self) -> bool:
        if not self.state.last_failure_time:
            return True
        elapsed = (datetime.utcnow() - self.state.last_failure_time).total_seconds()
        return elapsed >= self.state.recovery_timeout_seconds

    def execute(self, func: Callable, *args, **kwargs) -> dict:
        if not self.can_execute():
            return {
                "success": False,
                "circuit_state": self.state.state.value,
                "error": f"Circuit breaker '{self.state.name}' is OPEN",
                "fallback_needed": True
            }

        if self.state.state == CircuitState.HALF_OPEN:
            self.state.half_open_calls += 1

        try:
            result = func(*args, **kwargs)
            self.record_success()
            return {
                "success": True,
                "circuit_state": self.state.state.value,
                "result": result,
                "fallback_needed": False
            }
        except Exception as e:
            self.record_failure()
            return {
                "success": False,
                "circuit_state": self.state.state.value,
                "error": str(e),
                "fallback_needed": True
            }

    def get_status(self) -> dict:
        return {
            "name": self.state.name,
            "state": self.state.state.value,
            "failure_count": self.state.failure_count,
            "success_count": self.state.success_count,
            "failure_threshold": self.state.failure_threshold,
            "recovery_timeout_seconds": self.state.recovery_timeout_seconds,
            "last_failure": self.state.last_failure_time.isoformat()
            if self.state.last_failure_time else None,
            "half_open_calls": self.state.half_open_calls
        }

    def reset(self):
        self._close()
