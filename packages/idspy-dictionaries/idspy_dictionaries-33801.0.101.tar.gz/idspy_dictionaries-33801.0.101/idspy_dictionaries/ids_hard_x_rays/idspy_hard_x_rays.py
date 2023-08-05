# __version__= "033801.1.1"
# __version_data_dictionary__= "3.38.1"
# __git_version_hash__= "dd6854b4d073482810a23839e6e51386c7f20fd3"
# 
from ..dataclasses_idsschema import _IDSPYDD_USE_SLOTS,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass
class DetectorEnergyBand(IdsBaseClass):
    """
    Detector energy band.

    :ivar lower_bound: Lower bound of the energy band
    :ivar upper_bound: Upper bound of the energy band
    :ivar energies: Array of discrete energy values inside the band
    :ivar detection_efficiency: Probability of detection of a photon
        impacting the detector as a function of its energy
    """
    class Meta:
        name = "detector_energy_band"

    lower_bound: float = field(
        default=9e+40
    )
    upper_bound: float = field(
        default=9e+40
    )
    energies: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    detection_efficiency: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class HxrEmissivityProfile(IdsBaseClass):
    """
    Hard X-rays emissivity profile.

    :ivar lower_bound: Lower bound of the energy band
    :ivar upper_bound: Upper bound of the energy band
    :ivar rho_tor_norm: Normalised toroidal flux coordinate grid
    :ivar emissivity: Radial profile of the plasma emissivity in this
        energy band
    :ivar peak_position: Normalised toroidal flux coordinate position at
        which the emissivity peaks
    :ivar half_width_internal: Internal (towards magnetic axis) half
        width of the emissivity peak (in normalised toroidal flux)
    :ivar half_width_external: External (towards separatrix) half width
        of the emissivity peak (in normalised toroidal flux)
    :ivar validity_timed: Indicator of the validity of the emissivity
        profile data for each time slice. 0: valid from automated
        processing, 1: valid and certified by the diagnostic RO; - 1
        means problem identified in the data processing (request
        verification by the diagnostic RO), -2: invalid data, should not
        be used (values lower than -2 have a code-specific meaning
        detailing the origin of their invalidity)
    :ivar time: Time
    """
    class Meta:
        name = "hxr_emissivity_profile"

    lower_bound: float = field(
        default=9e+40
    )
    upper_bound: float = field(
        default=9e+40
    )
    rho_tor_norm: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    emissivity: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    peak_position: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    half_width_internal: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    half_width_external: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    validity_timed: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    time: Optional[str] = field(
        default=None
    )


@dataclass
class IdentifierStatic(IdsBaseClass):
    """Standard type for identifiers (static).

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
        name = "identifier_static"

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
class Rzphi0DStatic(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (0D, static)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi0d_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    phi: float = field(
        default=9e+40
    )


@dataclass
class SignalFlt2DValidity(IdsBaseClass):
    """
    Signal (FLT_2D) with its time base and validity flags.

    :ivar validity_timed: Indicator of the validity of the data for each
        time slice. 0: valid from automated processing, 1: valid and
        certified by the diagnostic RO; - 1 means problem identified in
        the data processing (request verification by the diagnostic RO),
        -2: invalid data, should not be used (values lower than -2 have
        a code-specific meaning detailing the origin of their
        invalidity)
    :ivar validity: Indicator of the validity of the data for the whole
        acquisition period. 0: valid from automated processing, 1: valid
        and certified by the diagnostic RO; - 1 means problem identified
        in the data processing (request verification by the diagnostic
        RO), -2: invalid data, should not be used (values lower than -2
        have a code-specific meaning detailing the origin of their
        invalidity)
    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_2d_validity"

    validity_timed: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    validity: int = field(
        default=999999999
    )
    time: Optional[str] = field(
        default=None
    )

    @dataclass
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_2D"
        )


@dataclass
class X1X21DStatic(IdsBaseClass):
    """
    Structure for list of X1, X2 positions (1D, static)

    :ivar x1: Positions along x1 axis
    :ivar x2: Positions along x2 axis
    """
    class Meta:
        name = "x1x21d_static"

    x1: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    x2: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass
class Xyz0DStatic(IdsBaseClass):
    """
    Structure for list of X, Y, Z components (0D, static)

    :ivar x: Component along X axis
    :ivar y: Component along Y axis
    :ivar z: Component along Z axis
    """
    class Meta:
        name = "xyz0d_static"

    x: float = field(
        default=9e+40
    )
    y: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
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
class DetectorAperture(IdsBaseClass):
    """
    Generic description of a plane detector or collimating aperture.

    :ivar geometry_type: Type of geometry used to describe the surface
        of the detector or aperture (1:'outline', 2:'circular',
        3:'rectangle'). In case of 'outline', the surface is described
        by an outline of point in a local coordinate system defined by a
        centre and three unit vectors X1, X2, X3. Note that there is
        some flexibility here and the data provider should choose the
        most convenient coordinate system for the object, respecting the
        definitions of (X1,X2,X3) indicated below. In case of
        'circular', the surface is a circle defined by its centre,
        radius, and normal vector oriented towards the plasma X3.  In
        case of 'rectangle', the surface is a rectangle defined by its
        centre, widths in the X1 and X2 directions, and normal vector
        oriented towards the plasma X3.
    :ivar centre: If geometry_type=2, coordinates of the centre of the
        circle. If geometry_type=1 or 3, coordinates of the origin of
        the local coordinate system (X1,X2,X3) describing the plane
        detector/aperture. This origin is located within the
        detector/aperture area.
    :ivar radius: Radius of the circle, used only if geometry_type = 2
    :ivar x1_unit_vector: Components of the X1 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X1 vector is more horizontal than X2 (has a
        smaller abs(Z) component) and oriented in the positive phi
        direction (counter-clockwise when viewing from above).
    :ivar x2_unit_vector: Components of the X2 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
        uX1.
    :ivar x3_unit_vector: Components of the X3 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X3 axis is normal to the detector/aperture
        plane and oriented towards the plasma.
    :ivar x1_width: Full width of the aperture in the X1 direction, used
        only if geometry_type = 3
    :ivar x2_width: Full width of the aperture in the X2 direction, used
        only if geometry_type = 3
    :ivar outline: Irregular outline of the detector/aperture in the
        (X1, X2) coordinate system. Do NOT repeat the first point.
    :ivar surface: Surface of the detector/aperture, derived from the
        above geometric data
    """
    class Meta:
        name = "detector_aperture"

    geometry_type: int = field(
        default=999999999
    )
    centre: Optional[Rzphi0DStatic] = field(
        default=None
    )
    radius: float = field(
        default=9e+40
    )
    x1_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x2_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x3_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x1_width: float = field(
        default=9e+40
    )
    x2_width: float = field(
        default=9e+40
    )
    outline: Optional[X1X21DStatic] = field(
        default=None
    )
    surface: float = field(
        default=9e+40
    )


@dataclass
class FilterWindow(IdsBaseClass):
    """
    Characteristics of the filter window (largely derived from curved_object), with
    some filter specific additions.

    :ivar identifier: ID of the filter
    :ivar geometry_type: Geometry of the filter contour. Note that there
        is some flexibility in the choice of the local coordinate system
        (X1,X2,X3). The data provider should choose the most convenient
        coordinate system for the filter, respecting the definitions of
        (X1,X2,X3) indicated below.
    :ivar curvature_type: Curvature of the filter.
    :ivar centre: Coordinates of the origin of the local coordinate
        system (X1,X2,X3) describing the filter. This origin is located
        within the filter area and should be the middle point of the
        filter surface. If geometry_type=2, it's the centre of the
        circular filter. If geometry_type=3, it's the centre of the
        rectangular filter.
    :ivar radius: Radius of the circle, used only if geometry_type/index
        = 2
    :ivar x1_unit_vector: Components of the X1 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X1 vector is more horizontal than X2 (has a
        smaller abs(Z) component) and oriented in the positive phi
        direction (counter-clockwise when viewing from above).
    :ivar x2_unit_vector: Components of the X2 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
        uX1.
    :ivar x3_unit_vector: Components of the X3 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X3 axis is normal to the filter surface and
        oriented towards the plasma.
    :ivar x1_width: Full width of the filter in the X1 direction, used
        only if geometry_type/index = 3
    :ivar x2_width: Full width of the filter in the X2 direction, used
        only if geometry_type/index = 3
    :ivar outline: Irregular outline of the filter in the (X1, X2)
        coordinate system, used only if geometry_type/index=1. Do NOT
        repeat the first point.
    :ivar x1_curvature: Radius of curvature in the X1 direction, to be
        filled only for curvature_type/index = 2, 4 or 5
    :ivar x2_curvature: Radius of curvature in the X2 direction, to be
        filled only for curvature_type/index = 3 or 5
    :ivar surface: Surface of the filter, derived from the above
        geometric data
    :ivar material: Material of the filter window
    :ivar thickness: Thickness of the filter window
    :ivar wavelength_lower: Lower bound of the filter wavelength range
    :ivar wavelength_upper: Upper bound of the filter wavelength range
    :ivar wavelengths: Array of wavelength values
    :ivar photon_absorption: Probability of absorbing a photon passing
        through the filter as a function of its wavelength
    """
    class Meta:
        name = "filter_window"

    identifier: str = field(
        default=""
    )
    geometry_type: Optional[IdentifierStatic] = field(
        default=None
    )
    curvature_type: Optional[IdentifierStatic] = field(
        default=None
    )
    centre: Optional[Rzphi0DStatic] = field(
        default=None
    )
    radius: float = field(
        default=9e+40
    )
    x1_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x2_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x3_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x1_width: float = field(
        default=9e+40
    )
    x2_width: float = field(
        default=9e+40
    )
    outline: Optional[X1X21DStatic] = field(
        default=None
    )
    x1_curvature: float = field(
        default=9e+40
    )
    x2_curvature: float = field(
        default=9e+40
    )
    surface: float = field(
        default=9e+40
    )
    material: Optional[IdentifierStatic] = field(
        default=None
    )
    thickness: float = field(
        default=9e+40
    )
    wavelength_lower: float = field(
        default=9e+40
    )
    wavelength_upper: float = field(
        default=9e+40
    )
    wavelengths: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    photon_absorption: list[ndarray[(int,), float]] = field(
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
class LineOfSight2Points(IdsBaseClass):
    """
    Generic description of a line of sight, defined by two points.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    """
    class Meta:
        name = "line_of_sight_2points"

    first_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    second_point: Optional[Rzphi0DStatic] = field(
        default=None
    )


@dataclass
class HxrChannel(IdsBaseClass):
    """
    Hard X-rays channel.

    :ivar name: Name of the channel
    :ivar identifier: ID of the channel
    :ivar detector: Detector description
    :ivar aperture: Description of a set of collimating apertures
    :ivar etendue: Etendue (geometric extent) of the channel's optical
        system
    :ivar etendue_method: Method used to calculate the etendue. Index =
        0 : exact calculation with a 4D integral; 1 : approximation with
        first order formula (detector surface times solid angle
        subtended by the apertures); 2 : other methods
    :ivar line_of_sight: Description of the line of sight of the
        channel, given by 2 points
    :ivar filter_window: Set of filter windows
    :ivar energy_band: Set of energy bands in which photons are counted
        by the detector
    :ivar radiance: Photons received by the detector per unit time, per
        unit solid angle and per unit area (i.e. photon flux divided by
        the etendue), in multiple energy bands if available from the
        detector
    """
    class Meta:
        name = "hxr_channel"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    detector: Optional[DetectorAperture] = field(
        default=None
    )
    aperture: list[DetectorAperture] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    etendue: float = field(
        default=9e+40
    )
    etendue_method: Optional[IdentifierStatic] = field(
        default=None
    )
    line_of_sight: Optional[LineOfSight2Points] = field(
        default=None
    )
    filter_window: list[FilterWindow] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    energy_band: list[DetectorEnergyBand] = field(
        default_factory=list,
        metadata={
            "max_occurs": 8,
        }
    )
    radiance: Optional[SignalFlt2DValidity] = field(
        default=None
    )


@dataclass
class HardXRays(IdsBaseClass):
    """
    Hard X-rays tomography diagnostic.

    :ivar ids_properties:
    :ivar channel: Set of channels (detector or pixel of a camera)
    :ivar emissivity_profile_1d: Emissivity profile per energy band
        (assumed common to all channels used in the profile
        reconstruction)
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "hard_x_rays"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    channel: list[HxrChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 60,
        }
    )
    emissivity_profile_1d: list[HxrEmissivityProfile] = field(
        default_factory=list,
        metadata={
            "max_occurs": 8,
        }
    )
    latency: float = field(
        default=9e+40
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
