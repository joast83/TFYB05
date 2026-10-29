"""Lägeshantering: vilka visningslägen varje uppgift stöder."""

from .core import *
from .problems import *

FIELD_OR_POTENTIAL = (
    ChargedRingAxis, SphericalShellPotential, ConcentricSphericalShells,
    FiniteLineCharge2D, CoaxialTubeSpaceCharge, SphericalCapacitorDesign,
    ConcentricChargedCylinders, CoaxialCylinderVoltage, OffsetCavitySphereExterior,
    SphericalConductorBreakdown, HClDipoleField, ChargedDielectricShell,
    RadialChargeSphere, PermanentlyMagnetizedCylinderAxis, AtmosphericChargeDensity,
    UniformSpaceChargePlates,
)
FIELD_OR_D = (
    DielectricSlabCapacitor, ElectretCylinderAxis, DielectricFilledSphericalGap,
    PorcelainSlabCapacitor, CoaxialTwoDielectricCapacitance,
    ObliqueConductorDielectricBoundary, VariableSigmaCoaxialElectrolyte,
)
FIELD_OR_MAGNITUDE = (
    SemiCircularSurfaceAxis, InsertedMetalPlateCapacitor,
    ThundercloudEnergyEstimate, GroundedInnerSphereChargeSplit,
    BreakdownVoltageCases, MakrofolCapacitorDesign, CircularArcOnAxis,
    ChargedSpheresSmallAngle, SphericalShellChargingEnergy,
    ParallelPlateForceDistance, CopperFoilLevitationEbonite,
    CylindricalCapacitorDielectricPullIn, PointChargeConductingPlane,
    ConductiveCoaxialElectrodes, CoaxialCableLeakage,
    SemicylindricalRingResistor, SteadyCurrentInterfaceCharge,
    HorseshoeMagnetAnchorForce, DisplacementCurrentCapacitor,
)
FIELD_OR_MAP = (
    FiniteWireBiotSavart, RotatingChargedDisk, SquareLoopOnAxis,
    RightAngleWireCorner, ElectronOrbitDipoleMoment,
    CircularLoopTorqueUniformField, DipoleDipoleTorque, AntarcticIceFlux,
    CopperWireMagneticLevitation, PermanentlyMagnetizedCylinderAxis,
    ThinCurrentStripField, LoopDipoleApproximationError,
    InfiniteWireRectangularLoopFlux, PermanentMagnetAirGapBHCurve,
    NonlinearIronMagneticCircuit, MagneticBridgeCircuit,
    CurrentCarryingMagneticTube, MagnetizationCurrentsCylinder,
    MutualInductanceParallelWiresSquare, MutualInductanceCoaxialLoops,
    OpenSecondaryTransformerVoltage, MovingLoopFieldWork, MovingLoopDipoleEmf,
    RadialChargeExpansionMaxwellTest,
)
SUPPORTS_TRUE_MAP = (
    ChargedRingAxis, FiniteLineCharge2D, SphericalShellPotential,
    ConcentricChargedCylinders, ConcentricSphericalShells, CoaxialCylinderVoltage,
    HClDipoleField, PorcelainSlabCapacitor, ChargedDielectricShell,
    DielectricFilledSphericalGap, DielectricSlabCapacitor,
    ThundercloudEnergyEstimate, FiniteWireBiotSavart, RotatingChargedDisk,
    SquareLoopOnAxis, RightAngleWireCorner, UniformSpaceChargePlates,
    ObliqueConductorDielectricBoundary, InfiniteWireRectangularLoopFlux,
)




def mode_options_for_problem(problem):
    """Returnerar synliga lägesnamn och motsvarande interna lägen för en uppgift."""
    special_options = (
        (ElectronOrbitDipoleMoment, [('Dipolmoment mot hastighet', 'Field'), ('Moment mot radie och hastighet', 'Map')]),
        (CircularLoopTorqueUniformField, [('Momentbidrag runt slingan', 'Field'), ('Moment mot ström och fält', 'Map')]),
        (DipoleDipoleTorque, [('Signerat moment mot vinkel', 'Field'), ('Momentbelopp mot vinkel och avstånd', 'Map')]),
        (LoopDipoleApproximationError, [('Relativt fel', 'Field'), ('Exakt fält och dipolfält', 'Map')]),
        (AntarcticIceFlux, [('Flöde mot latitudgräns', 'Field'), ('Flöde mot latitud och dipolmoment', 'Map')]),
        (CopperWireMagneticLevitation, [('Kraftbalans', 'Field'), ('Krävt fält mot strömtäthet och densitet', 'Map')]),
        (InfiniteWireRectangularLoopFlux, [('Normalkomponent Bz och flöde', 'Field'), ('Bz över slingytan', 'Map')]),
        (ConductiveCoaxialElectrodes, [('Elektriskt fält E', 'Field'), ('Strömtäthet J', 'Magnitude')]),
        (CoaxialCableLeakage, [('Läckström I', 'Field'), ('Effektförlust P', 'Magnitude')]),
        (VariableSigmaCoaxialElectrolyte, [('Elektriskt fält E', 'Field'), ('Strömtäthet J', 'Magnitude'), ('Fri laddningstäthet ρ', 'D')]),
        (SemicylindricalRingResistor, [('Resistans', 'Field')]),
        (SteadyCurrentInterfaceCharge, [('Fri ytladdning ρs', 'Field')]),
        (SphericalCapacitorDesign, [('Fältvillkor', 'Field'), ('Maxspänning', 'Potential')]),
        (AtmosphericChargeDensity, [('Fältprofil', 'Field'), ('Medelladdningstäthet', 'Potential')]),
        (BreakdownVoltageCases, [('Fältprofil', 'Field'), ('Umax-svep', 'Magnitude')]),
        (PermanentlyMagnetizedCylinderAxis, [('B-fält', 'Field'), ('H-fält', 'Potential'), ('Karta', 'Map')]),
    )
    for cls, options in special_options:
        if isinstance(problem, cls):
            return options
    options = [('Fält', 'Field')]
    if isinstance(problem, FIELD_OR_POTENTIAL):
        options.append(('Potential', 'Potential'))
    elif isinstance(problem, FIELD_OR_D):
        options.append(('D / flödestäthet', 'D'))
    elif isinstance(problem, FIELD_OR_MAGNITUDE):
        options.append(('Belopp / resultat', 'Magnitude'))
    elif isinstance(problem, FIELD_OR_MAP):
        options.append(('Karta / parameterstudie', 'Map'))
    if isinstance(problem, SUPPORTS_TRUE_MAP) and not any(internal == 'Map' for _, internal in options):
        options.append(('Karta', 'Map'))
    return options


def normalize_mode_for_problem(problem, requested_mode):
    """Normaliserar ett önskat internt läge till ett läge som uppgiften stöder."""
    if requested_mode == 'Potential / D':
        requested_mode = 'Potential'
    allowed = {internal for _, internal in mode_options_for_problem(problem)}
    if requested_mode in allowed:
        return requested_mode
    return 'Field'


