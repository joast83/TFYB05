"""Central lista över uppgifter i samma ordning som i programmenyn.

Ordningen här styr vad som visas i uppgiftsmenyn i gränssnittet. Siffran i
kommentaren efter varje rad är uppgiftens kapitel- och avsnittsnummer, för
att göra det lättare att hitta tillbaka till motsvarande kapitelmodul i
em_visualisering/problems/.
"""

from .problems import *

PROBLEMS = [
    ChargedSpheresSmallAngle(),  # 2.1
    ChargedRingAxis(),  # 2.2
    FiniteLineCharge2D(),  # 2.3
    SemiCircularSurfaceAxis(),  # 2.4
    SphericalShellPotential(),  # 2.5
    ConcentricChargedCylinders(),  # 2.6
    SphericalCapacitorDesign(),  # 2.7
    ConcentricSphericalShells(),  # 2.8
    AtmosphericChargeDensity(),  # 2.9
    OffsetCavitySphereExterior(),  # 2.10
    CoaxialCylinderVoltage(),  # 2.11
    SphericalConductorBreakdown(),  # 2.12
    CoaxialTubeSpaceCharge(),  # 2.13
    RadialChargeSphere(),  # 2.16
    InsertedMetalPlateCapacitor(),  # 2.18
    UniformSpaceChargePlates(),  # 2.19
    HClDipoleField(),  # 3.1
    PorcelainSlabCapacitor(),  # 3.3
    GroundedInnerSphereChargeSplit(),  # 3.6
    ChargedDielectricShell(),  # 3.7
    DielectricFilledSphericalGap(),  # 3.9
    MakrofolCapacitorDesign(),  # 3.11
    CoaxialTwoDielectricCapacitance(),  # 3.12
    BreakdownVoltageCases(),  # 3.13
    DielectricSlabCapacitor(),  # 3.14
    ElectretCylinderAxis(),  # 3.18
    ObliqueConductorDielectricBoundary(),  # 3.19
    SphericalShellChargingEnergy(),  # 4.1
    ParallelPlateForceDistance(),  # 4.2
    CopperFoilLevitationEbonite(),  # 4.3
    ThundercloudEnergyEstimate(),  # 4.5
    CylindricalCapacitorDielectricPullIn(),  # 4.6
    PointChargeConductingPlane(),  # 4.7
    ConductiveCoaxialElectrodes(),  # 5.1
    CoaxialCableLeakage(),  # 5.2
    VariableSigmaCoaxialElectrolyte(),  # 5.7
    SemicylindricalRingResistor(),  # 5.10
    SteadyCurrentInterfaceCharge(),  # 5.15
    FiniteWireBiotSavart(),  # 6.1
    SquareLoopOnAxis(),  # 6.2
    RightAngleWireCorner(),  # 6.3
    ThinCurrentStripField(),  # 6.5
    CircularArcOnAxis(),  # 6.8
    RotatingChargedDisk(),  # 6.13
    ElectronOrbitDipoleMoment(),  # 7.1
    CircularLoopTorqueUniformField(),  # 7.2
    DipoleDipoleTorque(),  # 7.3
    LoopDipoleApproximationError(),  # 7.5
    AntarcticIceFlux(),  # 7.6
    CopperWireMagneticLevitation(),  # 7.7
    InfiniteWireRectangularLoopFlux(),  # 7.10
    PermanentMagnetAirGapBHCurve(),  # 8.1
    NonlinearIronMagneticCircuit(),  # 8.2
    MagneticBridgeCircuit(),  # 8.4
    CurrentCarryingMagneticTube(),  # 8.5
    HorseshoeMagnetAnchorForce(),  # 8.6
    PermanentlyMagnetizedCylinderAxis(),  # 8.12
    MagnetizationCurrentsCylinder(),  # 8.13
    MutualInductanceParallelWiresSquare(),  # 9.2
    MutualInductanceCoaxialLoops(),  # 9.4
    OpenSecondaryTransformerVoltage(),  # 9.6
    MovingLoopFieldWork(),  # 9.13
    MovingLoopDipoleEmf(),  # 9.14
    DisplacementCurrentCapacitor(),  # 10.2
    RadialChargeExpansionMaxwellTest(),  # 10.3
]
