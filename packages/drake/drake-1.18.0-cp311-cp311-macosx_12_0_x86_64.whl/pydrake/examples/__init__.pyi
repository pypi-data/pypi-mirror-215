from typing import Any, ClassVar, Dict, List, Optional

from typing import overload
import numpy
import pydrake.common.eigen_geometry
import pydrake.geometry
import pydrake.math
import pydrake.multibody.plant
import pydrake.multibody.tree
import pydrake.systems.framework
import pydrake.systems.primitives
CreateClutterClearingYcbObjectList: function
CreateManipulationClassYcbObjectList: function
_xyz_rpy_deg: function
kBox: SchunkCollisionModel
kBoxCollision: IiwaCollisionModel
kBoxPlusFingertipSpheres: SchunkCollisionModel
kNoCollision: IiwaCollisionModel

class AcrobotGeometry(pydrake.systems.framework.LeafSystem):
    def __init__(self, *args, **kwargs) -> None: ...
    @overload
    @classmethod
    def AddToBuilder(cls, builder: pydrake.systems.framework.DiagramBuilder, acrobot_state_port: pydrake.systems.framework.OutputPort, acrobot_params: AcrobotParams, scene_graph: pydrake.geometry.SceneGraph) -> AcrobotGeometry: ...
    @overload
    @classmethod
    def AddToBuilder(cls, builder: pydrake.systems.framework.DiagramBuilder, acrobot_state_port: pydrake.systems.framework.OutputPort, scene_graph: pydrake.geometry.SceneGraph) -> AcrobotGeometry: ...

class AcrobotInput(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def set_tau(self, arg0: float) -> None: ...
    def tau(self) -> float: ...

class AcrobotParams(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def Ic1(self) -> float: ...
    def Ic2(self) -> float: ...
    def b1(self) -> float: ...
    def b2(self) -> float: ...
    def gravity(self) -> float: ...
    def l1(self) -> float: ...
    def lc1(self) -> float: ...
    def lc2(self) -> float: ...
    def m1(self) -> float: ...
    def m2(self) -> float: ...
    def set_Ic1(self, arg0: float) -> None: ...
    def set_Ic2(self, arg0: float) -> None: ...
    def set_b1(self, arg0: float) -> None: ...
    def set_b2(self, arg0: float) -> None: ...
    def set_gravity(self, arg0: float) -> None: ...
    def set_l1(self, arg0: float) -> None: ...
    def set_lc1(self, arg0: float) -> None: ...
    def set_lc2(self, arg0: float) -> None: ...
    def set_m1(self, arg0: float) -> None: ...
    def set_m2(self, arg0: float) -> None: ...

class AcrobotPlant(pydrake.systems.framework.LeafSystem):
    def __init__(self) -> None: ...
    def DynamicsBiasTerm(self, arg0: pydrake.systems.framework.Context) -> numpy.ndarray[numpy.float64[2,1]]: ...
    def MassMatrix(self, arg0: pydrake.systems.framework.Context) -> numpy.ndarray[numpy.float64[2,2]]: ...
    def SetMitAcrobotParameters(self, *args, **kwargs) -> Any: ...
    def get_mutable_parameters(self, *args, **kwargs) -> Any: ...
    @classmethod
    def get_mutable_state(cls, *args, **kwargs) -> Any: ...
    def get_parameters(self, *args, **kwargs) -> Any: ...
    @classmethod
    def get_state(cls, *args, **kwargs) -> Any: ...

class AcrobotSpongController(pydrake.systems.framework.LeafSystem):
    def __init__(self) -> None: ...
    def get_mutable_parameters(self, *args, **kwargs) -> Any: ...
    def get_parameters(self, *args, **kwargs) -> Any: ...

class AcrobotState(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def set_theta1(self, arg0: float) -> None: ...
    def set_theta1dot(self, arg0: float) -> None: ...
    def set_theta2(self, arg0: float) -> None: ...
    def set_theta2dot(self, arg0: float) -> None: ...
    def theta1(self) -> float: ...
    def theta1dot(self) -> float: ...
    def theta2(self) -> float: ...
    def theta2dot(self) -> float: ...

class CompassGait(pydrake.systems.framework.LeafSystem):
    def __init__(self) -> None: ...
    def get_floating_base_state_output_port(self) -> pydrake.systems.framework.OutputPort: ...
    def get_minimal_state_output_port(self) -> pydrake.systems.framework.OutputPort: ...

class CompassGaitContinuousState(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def set_stance(self, arg0: float) -> None: ...
    def set_stancedot(self, arg0: float) -> None: ...
    def set_swing(self, arg0: float) -> None: ...
    def set_swingdot(self, arg0: float) -> None: ...
    def stance(self) -> float: ...
    def stancedot(self) -> float: ...
    def swing(self) -> float: ...
    def swingdot(self) -> float: ...

class CompassGaitGeometry(pydrake.systems.framework.LeafSystem):
    def __init__(self, *args, **kwargs) -> None: ...
    @overload
    @classmethod
    def AddToBuilder(cls, builder: pydrake.systems.framework.DiagramBuilder, floating_base_state_port: pydrake.systems.framework.OutputPort, compass_gait_params: CompassGaitParams, scene_graph: pydrake.geometry.SceneGraph) -> CompassGaitGeometry: ...
    @overload
    @classmethod
    def AddToBuilder(cls, builder: pydrake.systems.framework.DiagramBuilder, floating_base_state_port: pydrake.systems.framework.OutputPort, scene_graph: pydrake.geometry.SceneGraph) -> CompassGaitGeometry: ...

class CompassGaitParams(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def center_of_mass_leg(self) -> float: ...
    def gravity(self) -> float: ...
    def length_leg(self) -> float: ...
    def mass_hip(self) -> float: ...
    def mass_leg(self) -> float: ...
    def set_center_of_mass_leg(self, arg0: float) -> None: ...
    def set_gravity(self, arg0: float) -> None: ...
    def set_length_leg(self, arg0: float) -> None: ...
    def set_mass_hip(self, arg0: float) -> None: ...
    def set_mass_leg(self, arg0: float) -> None: ...
    def set_slope(self, arg0: float) -> None: ...
    def slope(self) -> float: ...

class IiwaCollisionModel:
    __members__: ClassVar[dict] = ...  # read-only
    __entries: ClassVar[dict] = ...
    _pybind11_del_orig: ClassVar[None] = ...
    kBoxCollision: ClassVar[IiwaCollisionModel] = ...
    kNoCollision: ClassVar[IiwaCollisionModel] = ...
    def __init__(self, value: int) -> None: ...
    def __del__(self, *args, **kwargs) -> Any: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class ManipulationStation(pydrake.systems.framework.Diagram):
    def __init__(self, time_step: float = ...) -> None: ...
    def AddManipulandFromFile(self, model_file: str, X_WObject: pydrake.math.RigidTransform) -> None: ...
    @overload
    def Finalize(self) -> None: ...
    @overload
    def Finalize(self) -> Any: ...
    @overload
    def Finalize(self) -> Any: ...
    def GetIiwaPosition(self, arg0: pydrake.systems.framework.Context) -> numpy.ndarray[numpy.float64[m,1]]: ...
    def GetIiwaVelocity(self, arg0: pydrake.systems.framework.Context) -> numpy.ndarray[numpy.float64[m,1]]: ...
    def GetStaticCameraPosesInWorld(self) -> Dict[str,pydrake.math.RigidTransform]: ...
    def GetWsgPosition(self, arg0: pydrake.systems.framework.Context) -> float: ...
    def GetWsgVelocity(self, arg0: pydrake.systems.framework.Context) -> float: ...
    def RegisterIiwaControllerModel(self, arg0: str, arg1: pydrake.multibody.tree.ModelInstanceIndex, arg2: pydrake.multibody.tree.Frame, arg3: pydrake.multibody.tree.Frame, arg4: pydrake.math.RigidTransform) -> None: ...
    @overload
    def RegisterRgbdSensor(self, arg0: str, arg1: pydrake.multibody.tree.Frame, arg2: pydrake.math.RigidTransform, arg3: pydrake.geometry.DepthRenderCamera) -> None: ...
    @overload
    def RegisterRgbdSensor(self, arg0: str, arg1: pydrake.multibody.tree.Frame, arg2: pydrake.math.RigidTransform, arg3: pydrake.geometry.ColorRenderCamera, arg4: pydrake.geometry.DepthRenderCamera) -> None: ...
    def RegisterWsgControllerModel(self, arg0: str, arg1: pydrake.multibody.tree.ModelInstanceIndex, arg2: pydrake.multibody.tree.Frame, arg3: pydrake.multibody.tree.Frame, arg4: pydrake.math.RigidTransform) -> None: ...
    def SetIiwaIntegralGains(self, arg0: numpy.ndarray[numpy.float64[m,1]]) -> None: ...
    def SetIiwaPosition(self, station_context: pydrake.systems.framework.Context, q: numpy.ndarray[numpy.float64[m,1]]) -> None: ...
    def SetIiwaPositionGains(self, arg0: numpy.ndarray[numpy.float64[m,1]]) -> None: ...
    def SetIiwaVelocity(self, station_context: pydrake.systems.framework.Context, v: numpy.ndarray[numpy.float64[m,1]]) -> None: ...
    def SetIiwaVelocityGains(self, arg0: numpy.ndarray[numpy.float64[m,1]]) -> None: ...
    def SetWsgGains(self, arg0: float, arg1: float) -> None: ...
    def SetWsgPosition(self, station_context: pydrake.systems.framework.Context, q: float) -> None: ...
    def SetWsgVelocity(self, station_context: pydrake.systems.framework.Context, v: float) -> None: ...
    def SetupClutterClearingStation(self, X_WCameraBody: Optional[pydrake.math.RigidTransform] = ..., collision_model: IiwaCollisionModel = ..., schunk_model: SchunkCollisionModel = ...) -> None: ...
    def SetupManipulationClassStation(self, collision_model: IiwaCollisionModel = ..., schunk_model: SchunkCollisionModel = ...) -> None: ...
    def SetupPlanarIiwaStation(self, schunk_model: SchunkCollisionModel = ...) -> None: ...
    def get_camera_names(self) -> List[str]: ...
    def get_controller_plant(self) -> pydrake.multibody.plant.MultibodyPlant: ...
    def get_multibody_plant(self) -> pydrake.multibody.plant.MultibodyPlant: ...
    def get_mutable_multibody_plant(self) -> pydrake.multibody.plant.MultibodyPlant: ...
    def get_mutable_scene_graph(self) -> pydrake.geometry.SceneGraph: ...
    def get_scene_graph(self) -> pydrake.geometry.SceneGraph: ...
    def num_iiwa_joints(self) -> int: ...

class ManipulationStationHardwareInterface(pydrake.systems.framework.Diagram):
    def __init__(self, camera_names: List[str] = ...) -> None: ...
    def Connect(self, wait_for_cameras: bool = ...) -> None: ...
    def get_camera_names(self) -> List[str]: ...
    def get_controller_plant(self) -> pydrake.multibody.plant.MultibodyPlant: ...
    def num_iiwa_joints(self) -> int: ...

class PendulumGeometry(pydrake.systems.framework.LeafSystem):
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    def AddToBuilder(cls, builder: pydrake.systems.framework.DiagramBuilder, pendulum_state_port: pydrake.systems.framework.OutputPort, scene_graph: pydrake.geometry.SceneGraph) -> PendulumGeometry: ...

class PendulumInput(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def set_tau(self, tau: float) -> None: ...
    def tau(self) -> float: ...
    def with_tau(self, tau: float) -> PendulumInput: ...

class PendulumParams(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def damping(self) -> float: ...
    def gravity(self) -> float: ...
    def length(self) -> float: ...
    def mass(self) -> float: ...
    def set_damping(self, damping: float) -> None: ...
    def set_gravity(self, gravity: float) -> None: ...
    def set_length(self, length: float) -> None: ...
    def set_mass(self, mass: float) -> None: ...
    def with_damping(self, damping: float) -> PendulumParams: ...
    def with_gravity(self, gravity: float) -> PendulumParams: ...
    def with_length(self, length: float) -> PendulumParams: ...
    def with_mass(self, mass: float) -> PendulumParams: ...

class PendulumPlant(pydrake.systems.framework.LeafSystem):
    def __init__(self) -> None: ...
    def get_mutable_parameters(self, *args, **kwargs) -> Any: ...
    @classmethod
    def get_mutable_state(cls, *args, **kwargs) -> Any: ...
    def get_parameters(self, *args, **kwargs) -> Any: ...
    @classmethod
    def get_state(cls, *args, **kwargs) -> Any: ...
    def get_state_output_port(self) -> pydrake.systems.framework.OutputPort: ...

class PendulumState(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def set_theta(self, theta: float) -> None: ...
    def set_thetadot(self, thetadot: float) -> None: ...
    def theta(self) -> float: ...
    def thetadot(self) -> float: ...
    def with_theta(self, theta: float) -> PendulumState: ...
    def with_thetadot(self, thetadot: float) -> PendulumState: ...

class QuadrotorGeometry(pydrake.systems.framework.LeafSystem):
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    def AddToBuilder(cls, builder: pydrake.systems.framework.DiagramBuilder, quadrotor_state_port: pydrake.systems.framework.OutputPort, scene_graph: pydrake.geometry.SceneGraph) -> QuadrotorGeometry: ...
    def get_frame_id(self) -> pydrake.geometry.FrameId: ...

class QuadrotorPlant(pydrake.systems.framework.LeafSystem):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, m_arg: float, L_arg: float, I_arg: numpy.ndarray[numpy.float64[3,3]], kF_arg: float, kM_arg: float) -> None: ...
    def force_constant(self) -> float: ...
    def g(self) -> float: ...
    def inertia(self) -> numpy.ndarray[numpy.float64[3,3]]: ...
    def length(self) -> float: ...
    def m(self) -> float: ...
    def moment_constant(self) -> float: ...

class RigidTransform:
    _pybind11_del_orig: ClassVar[None] = ...
    multiply: ClassVar[function] = ...
    __matmul__: ClassVar[function] = ...
    cast: Any
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: pydrake.math.RigidTransform) -> None: ...
    @overload
    def __init__(self, quaternion: pydrake.common.eigen_geometry.Quaternion, p: numpy.ndarray[numpy.float64[3,1]]) -> None: ...
    @overload
    def __init__(self, theta_lambda: pydrake.common.eigen_geometry.AngleAxis, p: numpy.ndarray[numpy.float64[3,1]]) -> None: ...
    @overload
    def __init__(self, p: numpy.ndarray[numpy.float64[3,1]]) -> None: ...
    @overload
    def __init__(self, pose: pydrake.common.eigen_geometry.Isometry3) -> None: ...
    @overload
    def __init__(self, pose: numpy.ndarray[numpy.float64[m,n]]) -> None: ...
    def GetAsIsometry3(self) -> pydrake.common.eigen_geometry.Isometry3: ...
    def GetAsMatrix34(self) -> numpy.ndarray[numpy.float64[3,4]]: ...
    def GetAsMatrix4(self) -> numpy.ndarray[numpy.float64[4,4]]: ...
    def GetMaximumAbsoluteDifference(self, other: pydrake.math.RigidTransform) -> float: ...
    def GetMaximumAbsoluteTranslationDifference(self, other: pydrake.math.RigidTransform) -> float: ...
    @classmethod
    def Identity(cls) -> pydrake.math.RigidTransform: ...
    def InvertAndCompose(self, other: pydrake.math.RigidTransform) -> pydrake.math.RigidTransform: ...
    def IsExactlyEqualTo(self, other: pydrake.math.RigidTransform) -> bool: ...
    def IsExactlyIdentity(self) -> bool: ...
    def IsNearlyEqualTo(self, other: pydrake.math.RigidTransform, tolerance: float) -> bool: ...
    @overload
    def IsNearlyIdentity(self, translation_tolerance: float) -> bool: ...
    @overload
    def IsNearlyIdentity(self) -> Any: ...
    def SetFromIsometry3(self, pose: pydrake.common.eigen_geometry.Isometry3) -> None: ...
    def SetIdentity(self) -> pydrake.math.RigidTransform: ...
    def cast𝓣AutoDiffXd𝓤(self, *args, **kwargs) -> Any: ...
    def cast𝓣Expression𝓤(self, *args, **kwargs) -> Any: ...
    def cast𝓣float𝓤(self) -> pydrake.math.RigidTransform: ...
    def inverse(self) -> pydrake.math.RigidTransform: ...
    def rotation(self, *args, **kwargs) -> Any: ...
    def set(self, *args, **kwargs) -> Any: ...
    @overload
    def set_rotation(self, quaternion: pydrake.common.eigen_geometry.Quaternion) -> None: ...
    @overload
    def set_rotation(self, theta_lambda: pydrake.common.eigen_geometry.AngleAxis) -> None: ...
    def set_translation(self, p: numpy.ndarray[numpy.float64[3,1]]) -> None: ...
    def translation(self) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def __copy__(self) -> pydrake.math.RigidTransform: ...
    def __deepcopy__(self, arg0: dict) -> pydrake.math.RigidTransform: ...
    def __del__(self, *args, **kwargs) -> Any: ...
    def __getstate__(self) -> numpy.ndarray[numpy.float64[3,4]]: ...
    def __setstate__(self, arg0: numpy.ndarray[numpy.float64[3,4]]) -> None: ...

class RimlessWheel(pydrake.systems.framework.LeafSystem):
    def __init__(self) -> None: ...
    @classmethod
    def calc_alpha(cls, *args, **kwargs) -> Any: ...
    def get_floating_base_state_output_port(self) -> pydrake.systems.framework.OutputPort: ...
    def get_minimal_state_output_port(self) -> pydrake.systems.framework.OutputPort: ...

class RimlessWheelContinuousState(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def set_theta(self, arg0: float) -> None: ...
    def set_thetadot(self, arg0: float) -> None: ...
    def theta(self) -> float: ...
    def thetadot(self) -> float: ...

class RimlessWheelGeometry(pydrake.systems.framework.LeafSystem):
    def __init__(self, *args, **kwargs) -> None: ...
    @overload
    @classmethod
    def AddToBuilder(cls, builder: pydrake.systems.framework.DiagramBuilder, floating_base_state_port: pydrake.systems.framework.OutputPort, rimless_wheel_params: RimlessWheelParams, scene_graph: pydrake.geometry.SceneGraph) -> RimlessWheelGeometry: ...
    @overload
    @classmethod
    def AddToBuilder(cls, builder: pydrake.systems.framework.DiagramBuilder, floating_base_state_port: pydrake.systems.framework.OutputPort, scene_graph: pydrake.geometry.SceneGraph) -> RimlessWheelGeometry: ...

class RimlessWheelParams(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def gravity(self) -> float: ...
    def length(self) -> float: ...
    def mass(self) -> float: ...
    def number_of_spokes(self) -> float: ...
    def set_gravity(self, arg0: float) -> None: ...
    def set_length(self, arg0: float) -> None: ...
    def set_mass(self, arg0: float) -> None: ...
    def set_number_of_spokes(self, arg0: float) -> None: ...
    def set_slope(self, arg0: float) -> None: ...
    def slope(self) -> float: ...

class RollPitchYaw:
    @overload
    def __init__(self, other: pydrake.math.RollPitchYaw) -> None: ...
    @overload
    def __init__(self, rpy: numpy.ndarray[numpy.float64[3,1]]) -> None: ...
    @overload
    def __init__(self, roll: float, pitch: float, yaw: float) -> None: ...
    @overload
    def __init__(self, R: pydrake.math.RotationMatrix) -> None: ...
    @overload
    def __init__(self, quaternion: pydrake.common.eigen_geometry.Quaternion) -> None: ...
    @overload
    def __init__(self, matrix: numpy.ndarray[numpy.float64[3,3]]) -> None: ...
    def CalcAngularVelocityInChildFromRpyDt(self, rpyDt: numpy.ndarray[numpy.float64[3,1]]) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def CalcAngularVelocityInParentFromRpyDt(self, rpyDt: numpy.ndarray[numpy.float64[3,1]]) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def CalcRotationMatrixDt(self, rpyDt: numpy.ndarray[numpy.float64[3,1]]) -> numpy.ndarray[numpy.float64[3,3]]: ...
    def CalcRpyDDtFromAngularAccelInChild(self, rpyDt: numpy.ndarray[numpy.float64[3,1]], alpha_AD_D: numpy.ndarray[numpy.float64[3,1]]) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def CalcRpyDDtFromRpyDtAndAngularAccelInParent(self, rpyDt: numpy.ndarray[numpy.float64[3,1]], alpha_AD_A: numpy.ndarray[numpy.float64[3,1]]) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def CalcRpyDtFromAngularVelocityInChild(self, w_AD_D: numpy.ndarray[numpy.float64[3,1]]) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def CalcRpyDtFromAngularVelocityInParent(self, w_AD_A: numpy.ndarray[numpy.float64[3,1]]) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def ToQuaternion(self) -> pydrake.common.eigen_geometry.Quaternion: ...
    def ToRotationMatrix(self) -> pydrake.math.RotationMatrix: ...
    def pitch_angle(self) -> float: ...
    def roll_angle(self) -> float: ...
    def vector(self) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def yaw_angle(self) -> float: ...
    def __copy__(self) -> pydrake.math.RollPitchYaw: ...
    def __deepcopy__(self, arg0: dict) -> pydrake.math.RollPitchYaw: ...
    def __getstate__(self) -> numpy.ndarray[numpy.float64[3,1]]: ...
    def __setstate__(self, arg0: numpy.ndarray[numpy.float64[3,1]]) -> None: ...

class SchunkCollisionModel:
    __members__: ClassVar[dict] = ...  # read-only
    __entries: ClassVar[dict] = ...
    _pybind11_del_orig: ClassVar[None] = ...
    kBox: ClassVar[SchunkCollisionModel] = ...
    kBoxPlusFingertipSpheres: ClassVar[SchunkCollisionModel] = ...
    def __init__(self, value: int) -> None: ...
    def __del__(self, *args, **kwargs) -> Any: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class SpongControllerParams(pydrake.systems.framework.BasicVector):
    def __init__(self) -> None: ...
    def balancing_threshold(self) -> float: ...
    def k_d(self) -> float: ...
    def k_e(self) -> float: ...
    def k_p(self) -> float: ...
    def set_balancing_threshold(self, arg0: float) -> None: ...
    def set_k_d(self, arg0: float) -> None: ...
    def set_k_e(self, arg0: float) -> None: ...
    def set_k_p(self, arg0: float) -> None: ...

class VanDerPolOscillator(pydrake.systems.framework.LeafSystem):
    def __init__(self) -> None: ...
    @classmethod
    def CalcLimitCycle(cls) -> numpy.ndarray[numpy.float64[2,n]]: ...
    def get_full_state_output_port(self) -> pydrake.systems.framework.OutputPort: ...
    def get_position_output_port(self) -> pydrake.systems.framework.OutputPort: ...

def StabilizingLQRController(quadrotor_plant: QuadrotorPlant, nominal_position: numpy.ndarray[numpy.float64[3,1]]) -> pydrake.systems.primitives.AffineSystem: ...
