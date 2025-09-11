from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Self, runtime_checkable


@runtime_checkable
class PhysicsAdapter(Protocol):
    """Protocol for physics backends used by the UI and training code.

    This intentionally minimal interface enables deterministic stepping during
    early prototyping, while allowing a future PyBullet-backed implementation.
    """

    def reset(self: Self, seed: int | None) -> None:
        """Reset internal state; apply seed if provided."""

    def start(self: Self, seed: int | None) -> None:
        """Start a new episode; apply seed if provided."""

    def stop(self: Self) -> None:
        """Stop the current episode if running."""

    def step(self: Self, num_steps: int) -> None:
        """Advance the simulation deterministically by the given number of steps."""

    @property
    def step_count(self: Self) -> int:
        """Total steps advanced in the current episode."""
        ...

    @property
    def last_seed(self: Self) -> int | None:
        """The last seed applied via reset/start, if any."""
        ...


@dataclass
class DeterministicCounterAdapter:
    """Trivial adapter used for UI scaffolding and tests.

    Maintains an integer counter that advances on each call to ``step``.
    """

    _step_count: int = 0
    _last_seed: int | None = None
    _running: bool = False

    def reset(self: Self, seed: int | None) -> None:
        self._running = False
        self._step_count = 0
        if seed is not None:
            self._last_seed = seed

    def start(self: Self, seed: int | None) -> None:
        self._running = True
        self._step_count = 0
        if seed is not None:
            self._last_seed = seed

    def stop(self: Self) -> None:
        self._running = False

    def step(self: Self, num_steps: int) -> None:
        if not self._running:
            return
        if num_steps <= 0:
            return
        self._step_count += num_steps

    @property
    def step_count(self: Self) -> int:
        return self._step_count

    @property
    def last_seed(self: Self) -> int | None:
        return self._last_seed
