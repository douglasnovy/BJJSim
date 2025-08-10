from __future__ import annotations

from bjjsim.physics.adapter import DeterministicCounterAdapter, PhysicsAdapter


def test_deterministic_counter_adapter_basic() -> None:
    adapter: PhysicsAdapter = DeterministicCounterAdapter()

    # Initial state
    assert adapter.step_count == 0
    assert adapter.last_seed is None

    # Reset with seed sets last_seed and keeps not running
    adapter.reset(seed=123)
    assert adapter.last_seed == 123
    assert adapter.step_count == 0

    # Stepping while not running should not change state
    adapter.step(5)
    assert adapter.step_count == 0

    # Start and step
    adapter.start(seed=None)
    adapter.step(2)
    adapter.step(3)
    assert adapter.step_count == 5

    # Stop prevents further increments
    adapter.stop()
    adapter.step(10)
    assert adapter.step_count == 5


