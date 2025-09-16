from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, ClassVar

from bjjsim.physics import DeterministicCounterAdapter, PhysicsAdapter


@dataclass(slots=True)
class ContinuousSpace:
    """Simple representation of a continuous box space.

    The class mirrors the small subset of Gymnasium's ``Box`` interface relied on
    by our tests and documentation.  It stores the uniform lower/upper bounds and
    exposes the shape of the space for light validation.
    """

    size: int
    low: float
    high: float

    def __post_init__(self) -> None:
        if self.size <= 0:
            msg = "size must be positive"
            raise ValueError(msg)
        if self.low >= self.high:
            msg = "low must be strictly less than high"
            raise ValueError(msg)

    @property
    def shape(self) -> tuple[int]:
        return (self.size,)

    def clip(self, values: Sequence[float]) -> list[float]:
        if len(values) != self.size:
            msg = f"expected {self.size} values, received {len(values)}"
            raise ValueError(msg)
        return [min(max(float(v), self.low), self.high) for v in values]


@dataclass(slots=True)
class DictSpace:
    """Mapping of agent identifiers to :class:`ContinuousSpace` definitions."""

    spaces: dict[str, ContinuousSpace] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.spaces:
            msg = "spaces must contain at least one entry"
            raise ValueError(msg)

    def __getitem__(self, key: str) -> ContinuousSpace:
        return self.spaces[key]

    def keys(self) -> list[str]:  # pragma: no cover - convenience
        return list(self.spaces.keys())


@dataclass(slots=True)
class EnvConfig:
    """Configuration for :class:`BJJMultiAgentEnv`.

    The defaults intentionally keep the observation and action spaces small while
    providing enough structure for deterministic testing.  Observation values are
    bounded so the environment can participate in automated validation and future
    RL experiments without additional wrappers.
    """

    agent_names: tuple[str, ...] = ("agent1", "agent2")
    observation_dim: int = 12
    observation_low: float = -1000.0
    observation_high: float = 1000.0
    action_dim: int = 6
    action_low: float = -1.0
    action_high: float = 1.0
    max_episode_steps: int = 200
    step_reward: float = 0.1
    energy_penalty_scale: float = 0.05
    physics_steps_per_action: int = 1

    def __post_init__(self) -> None:
        if not self.agent_names:
            msg = "agent_names must contain at least one agent"
            raise ValueError(msg)
        if self.observation_dim <= 0:
            msg = "observation_dim must be positive"
            raise ValueError(msg)
        if self.action_dim <= 0:
            msg = "action_dim must be positive"
            raise ValueError(msg)
        if self.observation_low >= self.observation_high:
            msg = "observation_low must be strictly less than observation_high"
            raise ValueError(msg)
        if self.action_low >= self.action_high:
            msg = "action_low must be strictly less than action_high"
            raise ValueError(msg)
        if self.max_episode_steps <= 0:
            msg = "max_episode_steps must be positive"
            raise ValueError(msg)
        if self.physics_steps_per_action <= 0:
            msg = "physics_steps_per_action must be positive"
            raise ValueError(msg)


class BJJMultiAgentEnv:
    """Deterministic, dependency-free environment scaffold for BJJSim.

    The environment exposes two symmetric agents and uses the deterministic
    :class:`~bjjsim.physics.DeterministicCounterAdapter` by default.  It encodes
    the current episode and physics step counts into the observations and
    applies a simple reward made of a constant "step" reward minus an energy
    penalty proportional to the L2 norm of each agent's action vector.  The goal
    is to provide a stable target for wiring up future physics integrations and
    self-play experiments while exercising the multi-agent plumbing.
    """

    metadata: ClassVar[dict[str, Any]] = {"render_modes": []}

    def __init__(
        self,
        config: EnvConfig | None = None,
        *,
        physics: PhysicsAdapter | None = None,
    ) -> None:
        self.config = config or EnvConfig()
        self._physics: PhysicsAdapter = physics or DeterministicCounterAdapter()
        self.agents: tuple[str, ...] = tuple(self.config.agent_names)

        obs_space = ContinuousSpace(
            size=self.config.observation_dim,
            low=self.config.observation_low,
            high=self.config.observation_high,
        )
        self.observation_space = DictSpace({agent: obs_space for agent in self.agents})

        action_space = ContinuousSpace(
            size=self.config.action_dim,
            low=self.config.action_low,
            high=self.config.action_high,
        )
        self.action_space = DictSpace({agent: action_space for agent in self.agents})

        self._seed_source = random.Random()
        self._rng: random.Random = random.Random()
        self._last_seed: int | None = None
        self._episode_step: int = 0
        self._total_steps: int = 0
        self._episode_running: bool = False
        self._last_actions: dict[str, list[float]] = {
            agent: [0.0] * self.config.action_dim for agent in self.agents
        }

    @property
    def physics(self) -> PhysicsAdapter:
        """Return the physics adapter used by the environment."""

        return self._physics

    @property
    def last_seed(self) -> int | None:
        """Return the last seed applied via :meth:`reset`."""

        return self._last_seed

    @property
    def episode_step_count(self) -> int:
        """Number of steps taken in the current episode."""

        return self._episode_step

    @property
    def total_steps(self) -> int:
        """Total steps executed across all episodes since instantiation."""

        return self._total_steps

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[dict[str, list[float]], dict[str, dict[str, Any]]]:
        del options  # Unused for API compatibility with Gymnasium-style resets.
        if seed is None:
            seed = self._seed_source.randrange(0, 2**32)
        self._rng = random.Random(seed)
        self._last_seed = int(seed)
        self._episode_step = 0
        self._episode_running = True
        self._last_actions = {agent: [0.0] * self.config.action_dim for agent in self.agents}

        self._physics.reset(seed)
        self._physics.start(seed)

        observations = self._build_observations()
        infos = {
            agent: {
                "step": self._episode_step,
                "seed": self._last_seed,
                "physics_step": self._physics.step_count,
            }
            for agent in self.agents
        }
        return observations, infos

    def step(
        self, actions: Mapping[str, Sequence[float]]
    ) -> tuple[
        dict[str, list[float]],
        dict[str, float],
        dict[str, bool],
        dict[str, bool],
        dict[str, dict[str, Any]],
    ]:
        if not self._episode_running:
            msg = "reset() must be called before step() and episode must be active"
            raise RuntimeError(msg)

        processed_actions = self._process_actions(actions)
        self._last_actions = processed_actions

        self._physics.step(self.config.physics_steps_per_action)
        self._episode_step += 1
        self._total_steps += 1

        observations = self._build_observations()
        rewards: dict[str, float] = {}
        infos: dict[str, dict[str, Any]] = {}

        for agent, action in processed_actions.items():
            step_reward = self.config.step_reward
            energy_penalty = -self.config.energy_penalty_scale * _l2_norm(action)
            total_reward = step_reward + energy_penalty
            rewards[agent] = total_reward
            infos[agent] = {
                "reward_components": {
                    "step_reward": step_reward,
                    "energy_penalty": energy_penalty,
                },
                "step": self._episode_step,
                "physics_step": self._physics.step_count,
            }

        terminated = {agent: False for agent in self.agents}
        truncated = {agent: False for agent in self.agents}

        if self._episode_step >= self.config.max_episode_steps:
            truncated = {agent: True for agent in self.agents}
            self._episode_running = False
            self._physics.stop()

        return observations, rewards, terminated, truncated, infos

    def close(self) -> None:  # pragma: no cover - defensive
        self._physics.stop()

    def _process_actions(self, actions: Mapping[str, Sequence[float]]) -> dict[str, list[float]]:
        if set(actions.keys()) != set(self.agents):
            msg = "actions must provide exactly one entry per agent"
            raise ValueError(msg)

        processed: dict[str, list[float]] = {}
        for agent, value in actions.items():
            space = self.action_space[agent]
            try:
                clipped = space.clip(value)
            except TypeError as exc:  # Non-iterable provided
                msg = f"action for {agent} must be an iterable of floats"
                raise ValueError(msg) from exc
            processed[agent] = clipped
        return processed

    def _build_observations(self) -> dict[str, list[float]]:
        obs: dict[str, list[float]] = {}
        base_step = float(self._episode_step)
        physics_step = float(self._physics.step_count)
        for idx, agent in enumerate(self.agents):
            vec = [0.0] * self.config.observation_dim
            vec[0] = base_step
            if self.config.observation_dim > 1:
                vec[1] = physics_step
            if self.config.observation_dim > 2:
                vec[2] = float(idx)
            if self.config.observation_dim > 3:
                remaining = self.config.observation_dim - 3
                for pos in range(remaining):
                    vec[3 + pos] = self._rng.uniform(
                        self.config.observation_low,
                        self.config.observation_high,
                    )
            obs[agent] = vec
        return obs


def _l2_norm(values: Sequence[float]) -> float:
    return math.sqrt(sum(float(v) ** 2 for v in values))


__all__ = [
    "ContinuousSpace",
    "DictSpace",
    "EnvConfig",
    "BJJMultiAgentEnv",
]
