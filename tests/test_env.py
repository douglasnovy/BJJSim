from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Mapping, cast

import pytest

from bjjsim.env import BJJMultiAgentEnv, EnvConfig
from bjjsim.physics import DeterministicCounterAdapter


def make_zero_actions(env: BJJMultiAgentEnv) -> dict[str, list[float]]:
    return {agent: [0.0 for _ in range(env.config.action_dim)] for agent in env.agents}


def l2_norm(values: Sequence[float]) -> float:
    return math.sqrt(sum(float(v) ** 2 for v in values))


def test_reset_returns_deterministic_observations() -> None:
    env_a = BJJMultiAgentEnv()
    obs_a, info_a = env_a.reset(seed=123)
    env_b = BJJMultiAgentEnv()
    obs_b, info_b = env_b.reset(seed=123)

    assert set(obs_a.keys()) == set(env_a.agents)
    assert set(obs_b.keys()) == set(env_b.agents)
    for agent in env_a.agents:
        assert obs_a[agent] == pytest.approx(obs_b[agent], rel=0, abs=1e-9)
        assert info_a[agent]["seed"] == info_b[agent]["seed"] == env_a.last_seed == env_b.last_seed
        assert len(obs_a[agent]) == env_a.config.observation_dim
        assert all(isinstance(v, float) for v in obs_a[agent])

    # Stepping with identical actions should remain deterministic.
    actions = make_zero_actions(env_a)
    obs_next_a, _, _, _, _ = env_a.step(actions)
    obs_next_b, _, _, _, _ = env_b.step(actions)
    for agent in env_a.agents:
        assert obs_next_a[agent] == pytest.approx(obs_next_b[agent], rel=0, abs=1e-9)

    env_a.close()
    env_b.close()


def test_step_advances_physics_and_tracks_rewards() -> None:
    config = EnvConfig(max_episode_steps=3, physics_steps_per_action=2)
    physics = DeterministicCounterAdapter()
    env = BJJMultiAgentEnv(config=config, physics=physics)
    env.reset(seed=7)

    zero_actions = make_zero_actions(env)
    obs, rewards, terminated, truncated, infos = env.step(zero_actions)

    assert env.episode_step_count == 1
    assert physics.step_count == 2  # physics_steps_per_action
    for agent in env.agents:
        assert rewards[agent] == pytest.approx(config.step_reward)
        assert terminated[agent] is False
        assert truncated[agent] is False
        comps = infos[agent]["reward_components"]
        assert comps["step_reward"] == pytest.approx(config.step_reward)
        assert comps["energy_penalty"] == pytest.approx(0.0)
        assert len(obs[agent]) == config.observation_dim

    # Apply non-zero action to exercise penalty.
    action_with_energy = {
        agent: [1.0 if idx == 0 else 0.0 for idx in range(env.config.action_dim)]
        for agent in env.agents
    }
    _, rewards_energy, _, _, infos_energy = env.step(action_with_energy)
    expected_penalty = -env.config.energy_penalty_scale * l2_norm(action_with_energy[env.agents[0]])
    for agent in env.agents:
        assert rewards_energy[agent] == pytest.approx(env.config.step_reward + expected_penalty)
        assert infos_energy[agent]["reward_components"]["energy_penalty"] == pytest.approx(
            expected_penalty
        )

    # Continue stepping until we hit the max and trigger truncation.
    _, _, _, truncated_final, _ = env.step(zero_actions)
    assert all(truncated_final.values())
    with pytest.raises(RuntimeError):
        env.step(zero_actions)

    env.close()


def test_invalid_actions_raise() -> None:
    env = BJJMultiAgentEnv()
    env.reset(seed=5)

    wrong_shape = {agent: [0.0 for _ in range(env.config.action_dim + 1)] for agent in env.agents}
    with pytest.raises(ValueError):
        env.step(wrong_shape)

    missing_agent = {env.agents[0]: [0.0 for _ in range(env.config.action_dim)]}
    with pytest.raises(ValueError):
        env.step(missing_agent)

    # Non-iterable action values
    non_iterable_raw: dict[str, object] = {agent: 1.23 for agent in env.agents}
    with pytest.raises(ValueError):
        env.step(cast(Mapping[str, Sequence[float]], non_iterable_raw))

    env.close()
