import ctre
from wpilib import SmartDashboard as Dash
from wpilib.command import Subsystem

from constants import Constants
from utils import singleton, units, talonsrx, pidf


class BackArm(Subsystem, metaclass=singleton.Singleton):
    """The back arm subsystem controls the back arm motors and encoders."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize the back arm motors. This is not in the constructor to make the calling explicit in the robotInit to the robot simulator."""
        self.s_motor = talonsrx.TalonSRX(Constants.BS_MOTOR_ID)
        self.m_motor = talonsrx.TalonSRX(Constants.BM_MOTOR_ID)
        self.s_motor.initialize(inverted=False, encoder=False)
        self.m_motor.initialize(inverted=False, encoder=False)
        self.s_motor.follow(self.m_motor)
        self.m_motor.setPositionPIDF(
            Constants.BACK_ARM_KP, Constants.BACK_ARM_KI, Constants.BACK_ARM_KD, Constants.BACK_ARM_KF)

    def zeroSensors(self):
        """Set the encoder positions to 0."""
        self.m_motor.zero()

    def outputToSmartDashboard(self):
        self.s_motor.outputToDashboard()
        self.m_motor.outputToDashboard()

    def getAngle(self):
        """Get the angle of the arm in degrees."""
        self.m_motor.getPosition()

    def setAngle(self, angle):
        """Set the angle of the arm in degrees."""
        self.m_motor.setPositionSetpoint(angle)
