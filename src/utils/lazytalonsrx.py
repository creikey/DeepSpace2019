import ctre
import logging
from networktables import NetworkTables


class LazyTalonSRX(ctre.WPI_TalonSRX):
    """A wraper for the ctre.WPI_TalonSRX to simplfy configuration and getting/setting values."""
    MotorDash = NetworkTables.getTable(
        "SmartDashboard").getSubTable("TalonSRX")

    def __init__(self, id):
        super().__init__(id)
        self.no_encoder_warning = f"WARNING: No encoder connected to TalonSRX ({id})"

    def initialize(self, inverted=False, encoder=False, name=None):
        """Initialize the motors (enable the encoder, set invert status, set voltage limits)."""
        self.encoder = encoder
        if self.encoder:
            self.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, timeoutMs=10)
        self.setInverted(inverted)
        self.configNominalOutputForward(0, 5)
        self.configNominalOutputReverse(0, 5)
        self.configPeakOutputForward(1, 5)
        self.configPeakOutputReverse(-1, 5)
        if name != None:
            self.setName(name)

    def setVelocityPIDF(self, kp, ki, kd, kf):
        """Initialize the PIDF controler for velocity control."""
        self.selectProfileSlot(0, 0)
        self.config_kP(0, kp, 0)
        self.config_kI(0, ki, 0)
        self.config_kD(0, kd, 0)
        self.config_kF(0, kf, 0)

    def setVelocitySetpoint(self, velocity):
        """Set the velocity setpoint for the PIDF controler."""
        self.set(ctre.WPI_TalonSRX.ControlMode.Velocity, velocity)

    def setPositionPIDF(self, kp, ki, kd, kf):
        """Initialize the PIDF controler for position control."""
        self.selectProfileSlot(1, 0)
        self.config_kP(1, kp, 0)
        self.config_kI(1, ki, 0)
        self.config_kD(1, kd, 0)
        self.config_kF(1, kf, 0)

    def setPositionSetpoint(self, position):
        """Set the position setpoint for the PIDF controler."""
        self.set(ctre.WPI_TalonSRX.ControlMode.Position, position)

    def setPercentOutput(self, signal, max_signal=1):
        """Set the percent output of the motor."""
        signal = min(max(signal, -max_signal), max_signal)
        self.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput, signal)

    def zero(self):
        """Zero the encoder if it exists."""
        if self.encoder:
            self.setSelectedSensorPosition(0, 0, 0)
        else:
            logging.warning(self.no_encoder_warning)

    def getPosition(self):
        """Get the encoder position if it exists."""
        if self.encoder:
            return self.getSelectedSensorPosition(0)
        else:
            logging.warning(self.no_encoder_warning)
            return 0

    def getVelocity(self):
        """Get the encoder velocity if it exists."""
        if self.encoder:
            return self.getSelectedSensorVelocity(0)
        else:
            logging.warning(self.no_encoder_warning)
            return 0

    def outputToDashboard(self):
        self.MotorDash.putNumber(f"{self.name} Voltage", self.getBusVoltage())
        self.MotorDash.putNumber(f"{self.name} Percent Output",
                                 self.getMotorOutputPercent())
        self.MotorDash.putNumber(f"{self.name} Mode", self.getControlMode())

        if self.encoder:
            self.MotorDash.putNumber(
                f"{self.name} Position", self.getPosition())
            if self.getControlMode() == ctre.WPI_TalonSRX.ControlMode.Velocity or self.getControlMode() == ctre.WPI_TalonSRX.ControlMode.Position:
                self.MotorDash.putNumber(f"{self.name} PIDF Target",
                                         self.getClosedLoopTarget(0))
                self.MotorDash.putNumber(f"{self.name} PIDF Error",
                                         self.getClosedLoopError(0))