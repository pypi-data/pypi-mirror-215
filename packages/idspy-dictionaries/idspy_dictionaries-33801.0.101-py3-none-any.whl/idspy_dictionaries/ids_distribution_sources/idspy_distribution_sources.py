# __version__= "033801.1.1"
# __version_data_dictionary__= "3.38.1"
# __git_version_hash__= "dd6854b4d073482810a23839e6e51386c7f20fd3"
# 
from ..dataclasses_idsschema import _IDSPYDD_USE_SLOTS,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Dict, Optional


@dataclass
class BTorVacuum1(IdsBaseClass):
    """Characteristics of the vacuum toroidal field.

    Time coordinate at the root of the IDS

    :ivar r0: Reference major radius where the vacuum toroidal magnetic
        field is given (usually a fixed position such as the middle of
        the vessel at the equatorial midplane)
    :ivar b0: Vacuum toroidal field at R0 [T]; Positive sign means anti-
        clockwise when viewing from above. The product R0B0 must be
        consistent with the b_tor_vacuum_r field of the tf IDS.
    """
    class Meta:
        name = "b_tor_vacuum_1"

    r0: float = field(
        default=9e+40
    )
    b0: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class CoreRadialGrid(IdsBaseClass):
    """
    1D radial grid for core* IDSs.

    :ivar rho_tor_norm: Normalised toroidal flux coordinate. The
        normalizing value for rho_tor_norm, is the toroidal flux
        coordinate at the equilibrium boundary (LCFS or 99.x % of the
        LCFS in case of a fixed boundary equilibium calculation, see
        time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)
    :ivar rho_tor: Toroidal flux coordinate. rho_tor =
        sqrt(b_flux_tor/(pi*b0)) ~ sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The
        toroidal field used in its definition is indicated under
        vacuum_toroidal_field/b0
    :ivar rho_pol_norm: Normalised poloidal flux coordinate =
        sqrt((psi(rho)-psi(magnetic_axis)) /
        (psi(LCFS)-psi(magnetic_axis)))
    :ivar psi: Poloidal magnetic flux
    :ivar volume: Volume enclosed inside the magnetic surface
    :ivar area: Cross-sectional area of the flux surface
    :ivar surface: Surface area of the toroidal flux surface
    :ivar psi_magnetic_axis: Value of the poloidal magnetic flux at the
        magnetic axis (useful to normalize the psi array values when the
        radial grid doesn't go from the magnetic axis to the plasma
        boundary)
    :ivar psi_boundary: Value of the poloidal magnetic flux at the
        plasma boundary (useful to normalize the psi array values when
        the radial grid doesn't go from the magnetic axis to the plasma
        boundary)
    """
    class Meta:
        name = "core_radial_grid"

    rho_tor_norm: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    rho_tor: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    rho_pol_norm: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    psi: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    volume: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    area: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    surface: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    psi_magnetic_axis: float = field(
        default=9e+40
    )
    psi_boundary: float = field(
        default=9e+40
    )


@dataclass
class DistributionMarkersOrbit(IdsBaseClass):
    """Test particles for a given time slice : orbit integrals

    :ivar expressions: List of the expressions f(n_tor,m_pol,k,q,...)
        used in the orbit integrals
    :ivar n_tor: Array of toroidal mode numbers, n_tor, where quantities
        vary as exp(i.n_tor.phi) and phi runs anticlockwise when viewed
        from above
    :ivar m_pol: Array of poloidal mode numbers, where quantities vary
        as exp(-i.m_pol.theta) and theta is the angle defined by the
        choice of ../../coordinate_identifier, with its centre at the
        magnetic axis recalled at the root of this IDS
    :ivar bounce_harmonics: Array of bounce harmonics k
    :ivar values: Values of the orbit integrals
    """
    class Meta:
        name = "distribution_markers_orbit"

    expressions: Optional[list[str]] = field(
        default=None
    )
    n_tor: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    m_pol: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    bounce_harmonics: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    values: list[ndarray[(int, int, int, int, int), complex]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class DistributionMarkersOrbitInstant(IdsBaseClass):
    """Test particles for a given time slice : orbit integrals

    :ivar expressions: List of the expressions f(eq) used in the orbit
        integrals
    :ivar time_orbit: Time array along the markers last orbit
    :ivar values: Values of the orbit integrals
    """
    class Meta:
        name = "distribution_markers_orbit_instant"

    expressions: Optional[list[str]] = field(
        default=None
    )
    time_orbit: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    values: list[ndarray[(int, int, int ), complex]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class DistributionSourcesSourceGlobalShinethrough(IdsBaseClass):
    """
    Global quantities related to shinethrough, for a given time slice.

    :ivar power: Power losses due to shinethrough
    :ivar particles: Particle losses due to shinethrough
    :ivar torque_tor: Toroidal torque losses due to shinethrough
    """
    class Meta:
        name = "distribution_sources_source_global_shinethrough"

    power: float = field(
        default=9e+40
    )
    particles: float = field(
        default=9e+40
    )
    torque_tor: float = field(
        default=9e+40
    )


@dataclass
class GenericGridDynamicGridSubsetElementObject(IdsBaseClass):
    """
    Generic grid, object part of an element part of a grid_subset (dynamic within a
    type 3 AoS)

    :ivar space: Index of the space from which that object is taken
    :ivar dimension: Dimension of the object
    :ivar index: Object index
    """
    class Meta:
        name = "generic_grid_dynamic_grid_subset_element_object"

    space: int = field(
        default=999999999
    )
    dimension: int = field(
        default=999999999
    )
    index: int = field(
        default=999999999
    )


@dataclass
class GenericGridDynamicGridSubsetMetric(IdsBaseClass):
    """
    Generic grid, metric description for a given grid_subset and base (dynamic
    within a type 3 AoS)

    :ivar jacobian: Metric Jacobian
    :ivar tensor_covariant: Covariant metric tensor, given on each
        element of the subgrid (first dimension)
    :ivar tensor_contravariant: Contravariant metric tensor, given on
        each element of the subgrid (first dimension)
    """
    class Meta:
        name = "generic_grid_dynamic_grid_subset_metric"

    jacobian: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    tensor_covariant: list[ndarray[(int,int, int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    tensor_contravariant: list[ndarray[(int,int, int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class GenericGridDynamicSpaceDimensionObjectBoundary(IdsBaseClass):
    """
    Generic grid, description of an object boundary and its neighbours (dynamic
    within a type 3 AoS)

    :ivar index: Index of this (n-1)-dimensional boundary object
    :ivar neighbours: List of indices of the n-dimensional objects
        adjacent to the given n-dimensional object. An object can
        possibly have multiple neighbours on a boundary
    """
    class Meta:
        name = "generic_grid_dynamic_space_dimension_object_boundary"

    index: int = field(
        default=999999999
    )
    neighbours: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class GenericGridScalar(IdsBaseClass):
    """
    Scalar values on a generic grid (dynamic within a type 3 AoS)

    :ivar grid_index: Index of the grid used to represent this quantity
    :ivar grid_subset_index: Index of the grid subset the data is
        provided on
    :ivar values: One scalar value is provided per element in the grid
        subset.
    :ivar coefficients: Interpolation coefficients, to be used for a
        high precision evaluation of the physical quantity with finite
        elements, provided per element in the grid subset (first
        dimension).
    """
    class Meta:
        name = "generic_grid_scalar"

    grid_index: int = field(
        default=999999999
    )
    grid_subset_index: int = field(
        default=999999999
    )
    values: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    coefficients: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class Identifier(IdsBaseClass):
    """Standard type for identifiers (constant).

    The three fields: name, index and description are all
    representations of the same information. Associated with each
    application of this identifier-type, there should be a translation
    table defining the three fields for all objects to be identified.

    :ivar name: Short string identifier
    :ivar index: Integer identifier (enumeration index within a list).
        Private identifier values must be indicated by a negative index.
    :ivar description: Verbose description
    """
    class Meta:
        name = "identifier"

    name: str = field(
        default=""
    )
    index: int = field(
        default=999999999
    )
    description: str = field(
        default=""
    )


@dataclass
class IdentifierDynamicAos3(IdsBaseClass):
    """Standard type for identifiers (dynamic within type 3 array of structures
    (index on time)).

    The three fields: name, index and description are all
    representations of the same information. Associated with each
    application of this identifier-type, there should be a translation
    table defining the three fields for all objects to be identified.

    :ivar name: Short string identifier
    :ivar index: Integer identifier (enumeration index within a list).
        Private identifier values must be indicated by a negative index.
    :ivar description: Verbose description
    """
    class Meta:
        name = "identifier_dynamic_aos3"

    name: str = field(
        default=""
    )
    index: int = field(
        default=999999999
    )
    description: str = field(
        default=""
    )


@dataclass
class IdsProperties(IdsBaseClass):
    """Interface Data Structure properties.

    This element identifies the node above as an IDS

    :ivar comment: Any comment describing the content of this IDS
    :ivar homogeneous_time: This node must be filled (with 0, 1, or 2)
        for the IDS to be valid. If 1, the time of this IDS is
        homogeneous, i.e. the time values for this IDS are stored in the
        time node just below the root of this IDS. If 0, the time values
        are stored in the various time fields at lower levels in the
        tree. In the case only constant or static nodes are filled
        within the IDS, homogeneous_time must be set to 2
    :ivar provider: Name of the person in charge of producing this data
    :ivar creation_date: Date at which this data has been produced
    """
    class Meta:
        name = "ids_properties"

    comment: str = field(
        default=""
    )
    homogeneous_time: int = field(
        default=999999999
    )
    provider: str = field(
        default=""
    )
    creation_date: str = field(
        default=""
    )


@dataclass
class IdsProvenanceNode(IdsBaseClass):
    """
    Provenance information for a given node of the IDS.

    :ivar path: Path of the node within the IDS, following the syntax
        given in the link below. If empty, means the provenance
        information applies to the whole IDS.
    :ivar sources: List of sources used to import or calculate this
        node, identified as explained below. In case the node is the
        result of of a calculation / data processing, the source is an
        input to the process described in the "code" structure at the
        root of the IDS. The source can be an IDS (identified by a URI
        or a persitent identifier, see syntax in the link below) or non-
        IDS data imported directly from an non-IMAS database (identified
        by the command used to import the source, or the persistent
        identifier of the data source). Often data are obtained by a
        chain of processes, however only the last process input are
        recorded here. The full chain of provenance has then to be
        reconstructed recursively from the provenance information
        contained in the data sources.
    """
    class Meta:
        name = "ids_provenance_node"

    path: str = field(
        default=""
    )
    sources: Optional[list[str]] = field(
        default=None
    )


@dataclass
class Library(IdsBaseClass):
    """
    Library used by the code that has produced this IDS.

    :ivar name: Name of software
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    """
    class Meta:
        name = "library"

    name: str = field(
        default=""
    )
    commit: str = field(
        default=""
    )
    version: str = field(
        default=""
    )
    repository: str = field(
        default=""
    )
    parameters: str = field(
        default=""
    )


@dataclass
class PlasmaCompositionIonStateConstant(IdsBaseClass):
    """
    Definition of an ion state (when describing the plasma composition) (constant)

    :ivar z_min: Minimum Z of the charge state bundle (z_min = z_max = 0
        for a neutral)
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar label: String identifying ion state (e.g. C+, C+2 , C+3, C+4,
        C+5, C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    """
    class Meta:
        name = "plasma_composition_ion_state_constant"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    electron_configuration: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )


@dataclass
class PlasmaCompositionNeutralElementConstant(IdsBaseClass):
    """
    Element entering in the composition of the neutral atom or molecule (constant)

    :ivar a: Mass of atom
    :ivar z_n: Nuclear charge
    :ivar atoms_n: Number of atoms of this element in the molecule
    :ivar multiplicity: Multiplicity of the atom
    """
    class Meta:
        name = "plasma_composition_neutral_element_constant"

    a: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    atoms_n: int = field(
        default=999999999
    )
    multiplicity: float = field(
        default=9e+40
    )


@dataclass
class Rz1DDynamic1(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D, dynamic), time at the root of the
    IDS.

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz1d_dynamic_1"

    r: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    z: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class Code(IdsBaseClass):
    """
    Generic decription of the code-specific parameters for the code that has
    produced this IDS.

    :ivar name: Name of software generating IDS
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    :ivar output_flag: Output flag : 0 means the run is successful,
        other values mean some difficulty has been encountered, the
        exact meaning is then code specific. Negative values mean the
        result shall not be used.
    :ivar library: List of external libraries used by the code that has
        produced this IDS
    """
    class Meta:
        name = "code"

    name: str = field(
        default=""
    )
    commit: str = field(
        default=""
    )
    version: str = field(
        default=""
    )
    repository: str = field(
        default=""
    )
    parameters: str = field(
        default=""
    )
    output_flag: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    library: list[Library] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )


@dataclass
class DistributionMarkers(IdsBaseClass):
    """
    Test particles for a given time slice.

    :ivar coordinate_identifier: Set of coordinate identifiers,
        coordinates on which the markers are represented
    :ivar weights: Weight of the markers, i.e. number of real particles
        represented by each marker. The dimension of the vector
        correspond to the number of markers
    :ivar positions: Position of the markers in the set of coordinates.
        The first dimension corresponds to the number of markers, the
        second dimension to the set of coordinates
    :ivar orbit_integrals: Integrals along the markers orbit. These
        dimensionless expressions are of the form: (1/tau) integral
        (f(n_tor,m_pol,k,eq,...) dt) from time - tau to time, where tau
        is the transit/trapping time of the marker and f() a
        dimensionless function (phase factor,drift,etc) of the
        equilibrium (e.g. q) and perturbation (Fourier harmonics
        n_tor,m_pol and bounce harmonic k) along the particles orbits.
        In fact the integrals are taken during the last orbit of each
        marker at the time value of the time node below
    :ivar orbit_integrals_instant: Integrals/quantities along the
        markers orbit. These dimensionless expressions are of the form:
        (1/tau) integral ( f(eq) dt) from time - tau to time_orbit for
        different values of time_orbit in the interval from time - tau
        to time, where tau is the transit/trapping time of the marker
        and f(eq) a dimensionless function (phase, drift,q,etc) of the
        equilibrium along the markers orbits. The integrals are taken
        during the last orbit of each marker at the time value of the
        time node below
    :ivar toroidal_mode: In case the orbit integrals are calculated for
        a given MHD perturbation, index of the toroidal mode considered.
        Refers to the time_slice/toroidal_mode array of the MHD_LINEAR
        IDS in which this perturbation is described
    :ivar time: Time
    """
    class Meta:
        name = "distribution_markers"

    coordinate_identifier: list[IdentifierDynamicAos3] = field(
        default_factory=list
    )
    weights: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    positions: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    orbit_integrals: Optional[DistributionMarkersOrbit] = field(
        default=None
    )
    orbit_integrals_instant: Optional[DistributionMarkersOrbitInstant] = field(
        default=None
    )
    toroidal_mode: int = field(
        default=999999999
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass
class DistributionProcessIdentifier(IdsBaseClass):
    """
    Identifier an NBI or fusion reaction process intervening affecting a
    distribution function.

    :ivar type: Process type. index=1 for NBI; index=2 for nuclear
        reaction (reaction unspecified); index=3 for nuclear reaction:
        T(d,n)4He [D+T-&gt;He4+n]; index=4 for nuclear reaction:
        He3(d,p)4He [He3+D-&gt;He4+p]; index=5 for nuclear reaction:
        D(d,p)T [D+D-&gt;T+p]; index=6 for nuclear reaction: D(d,n)3He
        [D+D-&gt;He3+n]; index=7 for runaway processes
    :ivar reactant_energy: For nuclear reaction source, energy of the
        reactants. index = 0 for a sum over all energies; index = 1 for
        thermal-thermal; index = 2 for beam-beam; index = 3 for beam-
        thermal
    :ivar nbi_energy: For NBI source, energy of the accelerated species
        considered. index = 0 for a sum over all energies; index = 1 for
        full energiy; index = 2 for half energy; index = 3 for third
        energy
    :ivar nbi_unit: Index of the NBI unit considered. Refers to the
        "unit" array of the NBI IDS. 0 means sum over all NBI units.
    :ivar nbi_beamlets_group: Index of the NBI beamlets group
        considered. Refers to the "unit/beamlets_group" array of the NBI
        IDS. 0 means sum over all beamlets groups.
    """
    class Meta:
        name = "distribution_process_identifier"

    type: Optional[Identifier] = field(
        default=None
    )
    reactant_energy: Optional[Identifier] = field(
        default=None
    )
    nbi_energy: Optional[Identifier] = field(
        default=None
    )
    nbi_unit: int = field(
        default=999999999
    )
    nbi_beamlets_group: int = field(
        default=999999999
    )


@dataclass
class DistributionSourcesSourceGlobalQuantities(IdsBaseClass):
    """
    Global quantities of distribution_source for a given time slice.

    :ivar power: Total power of the source
    :ivar torque_tor: Total toroidal torque of the source
    :ivar particles: Particle source rate
    :ivar shinethrough: Shinethrough losses
    :ivar time: Time
    """
    class Meta:
        name = "distribution_sources_source_global_quantities"

    power: float = field(
        default=9e+40
    )
    torque_tor: float = field(
        default=9e+40
    )
    particles: float = field(
        default=9e+40
    )
    shinethrough: Optional[DistributionSourcesSourceGlobalShinethrough] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass
class DistributionSourcesSourceProfiles1D(IdsBaseClass):
    """
    Radial profile of source terms for a given time slice.

    :ivar grid: Radial grid
    :ivar energy: Source term for the energy transport equation
    :ivar momentum_tor: Source term for the toroidal momentum equation
    :ivar particles: Source term for the density transport equation
    :ivar time: Time
    """
    class Meta:
        name = "distribution_sources_source_profiles_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    energy: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    momentum_tor: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    particles: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass
class GenericGridDynamicGridSubsetElement(IdsBaseClass):
    """
    Generic grid, element part of a grid_subset (dynamic within a type 3 AoS)

    :ivar object_value: Set of objects defining the element
    """
    class Meta:
        name = "generic_grid_dynamic_grid_subset_element"

    object_value: list[GenericGridDynamicGridSubsetElementObject] = field(
        default_factory=list
    )


@dataclass
class GenericGridDynamicSpaceDimensionObject(IdsBaseClass):
    """
    Generic grid, list of objects of a given dimension within a space (dynamic
    within a type 3 AoS)

    :ivar boundary: Set of  (n-1)-dimensional objects defining the
        boundary of this n-dimensional object
    :ivar geometry: Geometry data associated with the object, its
        detailed content is defined by ../../geometry_content. Its
        dimension depends on the type of object, geometry and coordinate
        considered.
    :ivar nodes: List of nodes forming this object (indices to
        objects_per_dimension(1)%object(:) in Fortran notation)
    :ivar measure: Measure of the space object, i.e. physical size
        (length for 1d, area for 2d, volume for 3d objects,...)
    :ivar geometry_2d: 2D geometry data associated with the object. Its
        dimension depends on the type of object, geometry and coordinate
        considered. Typically, the first dimension represents the object
        coordinates, while the second dimension would represent the
        values of the various degrees of freedom of the finite element
        attached to the object.
    """
    class Meta:
        name = "generic_grid_dynamic_space_dimension_object"

    boundary: list[GenericGridDynamicSpaceDimensionObjectBoundary] = field(
        default_factory=list
    )
    geometry: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    nodes: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    measure: float = field(
        default=9e+40
    )
    geometry_2d: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class IdsProvenance(IdsBaseClass):
    """
    Provenance information about the IDS.

    :ivar node: Set of IDS nodes for which the provenance is given. The
        provenance information applies to the whole structure below the
        IDS node. For documenting provenance information for the whole
        IDS, set the size of this array of structure to 1 and leave the
        child "path" node empty
    """
    class Meta:
        name = "ids_provenance"

    node: list[IdsProvenanceNode] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )


@dataclass
class PlasmaCompositionIonsConstant(IdsBaseClass):
    """
    Description of plasma ions (constant)

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "plasma_composition_ions_constant"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    state: Optional[PlasmaCompositionIonStateConstant] = field(
        default=None
    )


@dataclass
class PlasmaCompositionNeutralStateConstant(IdsBaseClass):
    """
    Definition of a neutral state (when describing the plasma composition)
    (constant)

    :ivar label: String identifying neutral state
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    """
    class Meta:
        name = "plasma_composition_neutral_state_constant"

    label: str = field(
        default=""
    )
    electron_configuration: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    neutral_type: Optional[Identifier] = field(
        default=None
    )


@dataclass
class GenericGridDynamicGridSubset(IdsBaseClass):
    """
    Generic grid grid_subset (dynamic within a type 3 AoS)

    :ivar identifier: Grid subset identifier
    :ivar dimension: Space dimension of the grid subset elements. This
        must be equal to the sum of the dimensions of the individual
        objects forming the element.
    :ivar element: Set of elements defining the grid subset. An element
        is defined by a combination of objects from potentially all
        spaces
    :ivar base: Set of bases for the grid subset. For each base, the
        structure describes the projection of the base vectors on the
        canonical frame of the grid.
    :ivar metric: Metric of the canonical frame onto Cartesian
        coordinates
    """
    class Meta:
        name = "generic_grid_dynamic_grid_subset"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    dimension: int = field(
        default=999999999
    )
    element: list[GenericGridDynamicGridSubsetElement] = field(
        default_factory=list
    )
    base: list[GenericGridDynamicGridSubsetMetric] = field(
        default_factory=list
    )
    metric: Optional[GenericGridDynamicGridSubsetMetric] = field(
        default=None
    )


@dataclass
class GenericGridDynamicSpaceDimension(IdsBaseClass):
    """
    Generic grid, list of dimensions within a space (dynamic within a type 3 AoS)

    :ivar object_value: Set of objects for a given dimension
    :ivar geometry_content: Content of the ../object/geometry node for
        this dimension
    """
    class Meta:
        name = "generic_grid_dynamic_space_dimension"

    object_value: list[GenericGridDynamicSpaceDimensionObject] = field(
        default_factory=list
    )
    geometry_content: Optional[IdentifierDynamicAos3] = field(
        default=None
    )


@dataclass
class PlasmaCompositionNeutralConstant(IdsBaseClass):
    """
    Definition of plasma neutral (constant)

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar state: State of the species (energy, excitation, ...)
    """
    class Meta:
        name = "plasma_composition_neutral_constant"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    label: str = field(
        default=""
    )
    state: Optional[PlasmaCompositionNeutralStateConstant] = field(
        default=None
    )


@dataclass
class DistributionSpecies(IdsBaseClass):
    """
    Description of a species in a distribution function related IDS.

    :ivar type: Species type. index=1 for electron; index=2 for ion
        species in a single/average state (refer to ion structure);
        index=3 for ion species in a particular state (refer to
        ion/state structure);  index=4 for neutral species in a
        single/average state (refer to neutral structure); index=5 for
        neutral species in a particular state (refer to neutral/state
        structure);  index=6 for neutron; index=7 for photon
    :ivar ion: Description of the ion or neutral species, used if
        type/index = 2 or 3
    :ivar neutral: Description of the neutral species, used if
        type/index = 4 or 5
    """
    class Meta:
        name = "distribution_species"

    type: Optional[Identifier] = field(
        default=None
    )
    ion: Optional[PlasmaCompositionIonsConstant] = field(
        default=None
    )
    neutral: Optional[PlasmaCompositionNeutralConstant] = field(
        default=None
    )


@dataclass
class GenericGridDynamicSpace(IdsBaseClass):
    """
    Generic grid space (dynamic within a type 3 AoS)

    :ivar identifier: Space identifier
    :ivar geometry_type: Type of space geometry (0: standard, 1:Fourier,
        &gt;1: Fourier with periodicity)
    :ivar coordinates_type: Type of coordinates describing the physical
        space, for every coordinate of the space. The size of this node
        therefore defines the dimension of the space. The meaning of
        these predefined integer constants can be found in the Data
        Dictionary under utilities/coordinate_identifier.xml
    :ivar objects_per_dimension: Definition of the space objects for
        every dimension (from one to the dimension of the highest-
        dimensional objects). The index correspond to 1=nodes, 2=edges,
        3=faces, 4=cells/volumes, .... For every index, a collection of
        objects of that dimension is described.
    """
    class Meta:
        name = "generic_grid_dynamic_space"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    geometry_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    coordinates_type: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    objects_per_dimension: list[GenericGridDynamicSpaceDimension] = field(
        default_factory=list
    )


@dataclass
class GenericGridDynamic(IdsBaseClass):
    """
    Generic grid (dynamic within a type 3 AoS)

    :ivar identifier: Grid identifier
    :ivar path: Path of the grid, including the IDS name, in case of
        implicit reference to a grid_ggd node described in another IDS.
        To be filled only if the grid is not described explicitly in
        this grid_ggd structure. Example syntax:
        'wall:0/description_ggd(1)/grid_ggd', means that the grid is
        located in the wall IDS, occurrence 0, with ids path
        'description_ggd(1)/grid_ggd'. See the link below for more
        details about IDS paths
    :ivar space: Set of grid spaces
    :ivar grid_subset: Grid subsets
    """
    class Meta:
        name = "generic_grid_dynamic"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    path: str = field(
        default=""
    )
    space: list[GenericGridDynamicSpace] = field(
        default_factory=list
    )
    grid_subset: list[GenericGridDynamicGridSubset] = field(
        default_factory=list
    )


@dataclass
class DistributionSourcesSourceGgd(IdsBaseClass):
    """
    Source terms for a given time slice, using a GGD representation.

    :ivar grid: Grid description
    :ivar particles: Source density of particles in phase space, for
        various grid subsets
    :ivar discrete: List of indices of grid spaces (refers to
        ../grid/space) for which the source is discretely distributed.
        For example consider a source of 3.5 MeV alpha particles
        provided on a grid with two coordinates (spaces); rho_tor and
        energy. To specify that the source is given at energies exactly
        equal to 3.5 MeV, let discret have length 1 and set
        discrete(1)=2 since energy is dimension number 2. The source is
        then proportional to delta( 1 - energy / 3.5MeV ), where delta
        is the direct delta distribution. Discrete dimensions can only
        be used when the grid is rectangular.
    :ivar time: Time
    """
    class Meta:
        name = "distribution_sources_source_ggd"

    grid: Optional[GenericGridDynamic] = field(
        default=None
    )
    particles: list[GenericGridScalar] = field(
        default_factory=list
    )
    discrete: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass
class DistributionSourcesSource(IdsBaseClass):
    """
    Source terms for a given actuator.

    :ivar process: Set of processes (NBI units, fusion reactions, ...)
        that provide the source.
    :ivar gyro_type: Defines how to interpret the spatial coordinates: 1
        = given at the actual particle birth point; 2 =given at the gyro
        centre of the birth point
    :ivar species: Species injected or consumed by this source/sink
    :ivar global_quantities: Global quantities for various time slices
    :ivar profiles_1d: Source radial profiles (flux surface averaged
        quantities) for various time slices
    :ivar ggd: Source terms in phase space (real space, velocity space,
        spin state), represented using the ggd, for various time slices
    :ivar markers: Source given as a group of markers (test particles)
        born per second, for various time slices
    """
    class Meta:
        name = "distribution_sources_source"

    process: list[DistributionProcessIdentifier] = field(
        default_factory=list,
        metadata={
            "max_occurs": 32,
        }
    )
    gyro_type: int = field(
        default=999999999
    )
    species: Optional[DistributionSpecies] = field(
        default=None
    )
    global_quantities: list[DistributionSourcesSourceGlobalQuantities] = field(
        default_factory=list
    )
    profiles_1d: list[DistributionSourcesSourceProfiles1D] = field(
        default_factory=list
    )
    ggd: list[DistributionSourcesSourceGgd] = field(
        default_factory=list
    )
    markers: list[DistributionMarkers] = field(
        default_factory=list
    )


@dataclass
class DistributionSources(IdsBaseClass):
    """Sources of particles for input to kinetic equations, e.g. Fokker-Planck
    calculation.

    The sources could originate from e.g. NBI or fusion reactions.

    :ivar ids_properties:
    :ivar source: Set of source/sink terms. A source/sink term
        corresponds to the particle source due to an NBI injection unit,
        a nuclear reaction or any combination of them (described in
        "identifier")
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition)
    :ivar magnetic_axis: Magnetic axis position (used to define a
        poloidal angle for the 2D profiles)
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "distribution_sources"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    source: list[DistributionSourcesSource] = field(
        default_factory=list,
        metadata={
            "max_occurs": 33,
        }
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    magnetic_axis: Optional[Rz1DDynamic1] = field(
        default=None
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
