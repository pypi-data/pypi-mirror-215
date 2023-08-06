from typing import Dict, List, Mapping, Tuple
import numpy as np
from numpy.typing import NDArray

from mlagents_envs.base_env import (
    ActionTuple,
    BaseEnv,
    BehaviorMapping,
    DecisionSteps,
    TerminalSteps,
    BehaviorSpec,
    ActionSpec,
    ObservationSpec,
    DimensionProperty,
    ObservationType,
    BehaviorName,
    AgentId,
)

from TransformsAI.Animo.Learning.Sensors import SensorSpec
from TransformsAI.Animo.Learning.Sensors import SensorTypes
from TransformsAI.Animo.Rewards import RewardEvaluator
from TransformsAI.Animo.Learning.Sensors.Primitives import Sensor
from TransformsAI.Animo.Learning.Sensors.Primitives import VectorSensor
from TransformsAI.Animo.Learning.Sensors.Primitives import GridSensor
from TransformsAI.Animo.Learning.Sensors.Primitives import VariableLengthSensor

from System import Array, Single
from TransformsAI.Animo.Objects.Character import CharacterObject
from typing import cast

from animo_trainer.animo_training_session import AnimoTrainingSessionConfig
import animo_trainer.typed_numpy as tnp

ACTION_MASK = [tnp.zeros((1, 7), np.bool_)]
GROUP_ID = tnp.zeros((1,), dtype=np.int32)
GROUP_REWARD = tnp.zeros((1,), dtype=np.float32)


class AnimoEnv(BaseEnv):
    def __init__(self, training_session: AnimoTrainingSessionConfig):
        self.session = training_session

        self.voxel_grid = None
        self.end_conditions = self.session.level_data.EndConditions

        self.step_index: int = 0
        self.episode_index: int = 0
        self.will_reset_next_step = False

        self.behavior_mapping: BehaviorMapping
        self.agent_sensor_dict: Dict[int, List[Sensor]] = {}
        self.agent_reward_evaluators_dict: Dict[int, RewardEvaluator] = {}

        behaviour_specs: Dict[BehaviorName, BehaviorSpec] = {}

        for behaviour_name, agent_data in self.session.agent_datas.items():
            sensors: List[Sensor] = [sensor for sensor in agent_data.ConstructSensors()]
            self.agent_sensor_dict[agent_data.Id] = sensors

            reward_evaluator: RewardEvaluator = RewardEvaluator(int(behaviour_name), agent_data.CurrentRewards)
            self.agent_reward_evaluators_dict[agent_data.Id] = reward_evaluator

            obs_specs = [self.sensor_spec_to_observation_spec(sensor.SensorSpec, sensor.sensorConfig.sensorName) for sensor in sensors]
            action_spec = ActionSpec(continuous_size=0, discrete_branches=(7,))
            behavior_spec = BehaviorSpec(obs_specs, action_spec)
            behaviour_specs[behaviour_name] = behavior_spec

        self.behavior_mapping = BehaviorMapping(behaviour_specs)

    @staticmethod
    def sensor_spec_to_observation_spec(sensor_spec: SensorSpec, name: str) -> ObservationSpec:
        if sensor_spec.SensorType == SensorTypes.Vector:
            return ObservationSpec(
                name=name,
                shape=(sensor_spec.VectorLength,),
                dimension_property=(DimensionProperty.NONE,),
                observation_type=ObservationType.DEFAULT,
            )
        elif sensor_spec.SensorType == SensorTypes.Grid:
            grid_shape = sensor_spec.GridShape

            return ObservationSpec(
                name=name,
                shape=(grid_shape.XLength, grid_shape.ZLength, grid_shape.Depth),
                dimension_property=(DimensionProperty.TRANSLATIONAL_EQUIVARIANCE, DimensionProperty.TRANSLATIONAL_EQUIVARIANCE, DimensionProperty.NONE),
                observation_type=ObservationType.DEFAULT,
            )
        elif sensor_spec.SensorType == SensorTypes.VariableLen:
            return ObservationSpec(
                name=name,
                shape=(sensor_spec.VariableLenShape.Entities, sensor_spec.VariableLenShape.Properties),
                dimension_property=(DimensionProperty.VARIABLE_SIZE, DimensionProperty.NONE),
                observation_type=ObservationType.DEFAULT,
            )

    def reset(self) -> None:
        # we copy the session's grid to avoid modifying the original
        level_data = self.session.level_data
        self.voxel_grid = level_data.SavedGrid.Copy()

        for agent_reward_evaluator in self.agent_reward_evaluators_dict.values():
            self.voxel_grid.SimulationRunner.observers.Add(agent_reward_evaluator)

        level_data.BlockWiggle.WiggleBlocks(self.voxel_grid)
        level_data.CharacterWiggle.WiggleCharacters(self.voxel_grid)
        level_data.ObjectWiggle.WiggleObjects(self.voxel_grid)

    @property
    def behavior_specs(self) -> Mapping[BehaviorName, BehaviorSpec]:
        return self.behavior_mapping

    def get_steps(self, behavior_name: BehaviorName) -> Tuple[DecisionSteps, TerminalSteps]:
        (observations, reward, agent_id) = self.get_env_step_data(behavior_name)

        if self.will_reset_next_step:
            is_interrupted = tnp.zeros((1, 1), dtype=np.bool_)

            decision_steps = DecisionSteps.empty(self.behavior_mapping[behavior_name])
            terminal_steps = TerminalSteps(
                observations, reward, is_interrupted, agent_id, GROUP_ID, GROUP_REWARD
            )
        else:
            decision_steps = DecisionSteps(observations, reward, agent_id, ACTION_MASK, GROUP_ID, GROUP_REWARD)
            terminal_steps = TerminalSteps.empty(self.behavior_mapping[behavior_name])

        return (decision_steps, terminal_steps)

    def set_actions(self, behavior_name: BehaviorName, action: ActionTuple) -> None:
        if not self.will_reset_next_step:
            character = self.voxel_grid.GetCharacter(int(behavior_name))
            raw_action = int(action.discrete[0])  # type: ignore
            character.NextAction = CharacterObject.Actions(raw_action)

    def step(self) -> None:
        for reward_evaluator in self.agent_reward_evaluators_dict.values():
            reward_evaluator.ClearExecutionCounts()

        if self.will_reset_next_step:
            for accumulator in self.session.checkpoint_accumulators.values():
                accumulator.OnEpisodeEnded(self.step_index)
            self.reset()
            self.will_reset_next_step = False
            self.step_index = 0
            self.episode_index += 1
        else:
            self.voxel_grid.SimulationRunner.Simulate()
            self.step_index += 1
            if self.end_conditions.IsMet(self.voxel_grid, self.step_index):
                self.will_reset_next_step = True

    def get_env_step_data(self, behavior_name: BehaviorName) -> Tuple[
        List[NDArray[np.float32]],  # Observations
        NDArray[np.float32],  # Reward
        NDArray[np.int32],  # Agent ID
    ]:
        agent_data = self.session.agent_datas[behavior_name]
        character = self.voxel_grid.GetCharacter(agent_data.Id)

        agent_sensors = self.agent_sensor_dict[agent_data.Id]
        observations = []

        for agent_sensor in agent_sensors:
            if agent_sensor.sensorConfig.sensorSpec.SensorType == SensorTypes.Vector:
                agent_vector_sensor = cast(VectorSensor, agent_sensor)
                obs = Array.CreateInstance(Single, agent_vector_sensor.Length)
                agent_vector_sensor.GetObservations(character, obs)
                agent_vector_observation = tnp.array(obs, dtype=np.float32)
                observations.append(tnp.expand_dims(agent_vector_observation, axis=0))

            elif agent_sensor.sensorConfig.sensorSpec.SensorType == SensorTypes.Grid:
                agent_grid_sensor = cast(GridSensor, agent_sensor)
                obs = Array.CreateInstance(Single, agent_grid_sensor.GridShape.XLength, agent_grid_sensor.GridShape.ZLength, agent_grid_sensor.GridShape.Depth)
                agent_grid_sensor.GetGridObservations(character, obs)
                agent_grid_observation = tnp.array(obs, dtype=np.float32)
                observations.append(tnp.expand_dims(agent_grid_observation, axis=0))

            elif agent_sensor.sensorConfig.sensorSpec.SensorType == SensorTypes.VariableLen:
                agent_variable_length_sensor = cast(VariableLengthSensor, agent_sensor)
                obs = Array.CreateInstance(Single, agent_variable_length_sensor.NumEntities, agent_variable_length_sensor.EntitySize)
                agent_variable_length_sensor.GetEntitiesObservations(character, obs)
                agent_variable_length_observation = tnp.array(obs, dtype=np.float32)
                observations.append(tnp.expand_dims(agent_variable_length_observation, axis=0))

        reward = self.agent_reward_evaluators_dict[int(behavior_name)].GetTotalRewardThisStep()
        reward = tnp.multiply(tnp.ones((1,), dtype=np.float32), reward)

        agent_id = tnp.multiply(tnp.ones((1,), dtype=np.int32), self.episode_index)
        return (observations, reward, agent_id)

    def set_action_for_agent(self, behavior_name: BehaviorName, agent_id: AgentId, action: ActionTuple) -> None:
        # TODO: Explain why this isn't implemented
        pass

    def close(self) -> None:
        pass
