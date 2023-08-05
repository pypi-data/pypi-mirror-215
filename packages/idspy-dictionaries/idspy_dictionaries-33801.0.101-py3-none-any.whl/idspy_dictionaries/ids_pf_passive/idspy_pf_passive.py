# __version__= "033801.1.1"
# __version_data_dictionary__= "3.38.1"
# __git_version_hash__= "dd6854b4d073482810a23839e6e51386c7f20fd3"
# 
from ..dataclasses_idsschema import _IDSPYDD_USE_SLOTS,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass
class AnnulusStatic(IdsBaseClass):
    """
    Annulus description (2D object)

    :ivar r: Centre major radius
    :ivar z: Centre height
    :ivar radius_inner: Inner radius
    :ivar radius_outer: Outer radius
    """
    class Meta:
        name = "annulus_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    radius_inner: float = field(
        default=9e+40
    )
    radius_outer: float = field(
        default=9e+40
    )


@dataclass
class ArcsOfCircleStatic(IdsBaseClass):
    """
    Arcs of circle description of a 2D contour.

    :ivar r: Major radii of the start point of each arc of circle
    :ivar z: Height of the start point of each arc of circle
    :ivar curvature_radii: Curvature radius of each arc of circle
    """
    class Meta:
        name = "arcs_of_circle_static"

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
    curvature_radii: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
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
class ObliqueStatic(IdsBaseClass):
    """
    Description of a 2D parallelogram.

    :ivar r: Major radius of the reference point (from which the alpha
        and beta angles are defined, marked by a + on the diagram)
    :ivar z: Height of the reference point (from which the alpha and
        beta angles are defined, marked by a + on the diagram)
    :ivar length_alpha: Length of the parallelogram side inclined with
        angle alpha with respect to the major radius axis
    :ivar length_beta: Length of the parallelogram side inclined with
        angle beta with respect to the height axis
    :ivar alpha: Inclination of first angle measured counter-clockwise
        from horizontal outwardly directed radial vector (grad R).
    :ivar beta: Inclination of second angle measured counter-clockwise
        from vertically upwards directed vector (grad Z). If both alpha
        and beta are zero (rectangle) then the simpler rectangular
        elements description should be used.
    """
    class Meta:
        name = "oblique_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    length_alpha: float = field(
        default=9e+40
    )
    length_beta: float = field(
        default=9e+40
    )
    alpha: float = field(
        default=9e+40
    )
    beta: float = field(
        default=9e+40
    )


@dataclass
class RectangleStatic(IdsBaseClass):
    """
    Rectangular description of a 2D object.

    :ivar r: Geometric centre R
    :ivar z: Geometric centre Z
    :ivar width: Horizontal full width
    :ivar height: Vertical full height
    """
    class Meta:
        name = "rectangle_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    width: float = field(
        default=9e+40
    )
    height: float = field(
        default=9e+40
    )


@dataclass
class Rz0DStatic(IdsBaseClass):
    """
    Structure for a single R, Z position (0D, static)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz0d_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )


@dataclass
class Rz1DStatic(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D, constant)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz1d_static"

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
class ThickLineStatic(IdsBaseClass):
    """
    2D contour approximated by two points and a thickness (in the direction
    perpendicular to the segment) in the poloidal cross-section.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    :ivar thickness: Thickness
    """
    class Meta:
        name = "thick_line_static"

    first_point: Optional[Rz0DStatic] = field(
        default=None
    )
    second_point: Optional[Rz0DStatic] = field(
        default=None
    )
    thickness: float = field(
        default=9e+40
    )


@dataclass
class Outline2DGeometryStatic(IdsBaseClass):
    """
    Description of 2D geometry.

    :ivar geometry_type: Type used to describe the element shape
        (1:'outline', 2:'rectangle', 3:'oblique', 4:'arcs of circle, 5:
        'annulus', 6 : 'thick line')
    :ivar outline: Irregular outline of the element. Do NOT repeat the
        first point.
    :ivar rectangle: Rectangular description of the element
    :ivar oblique: Parallelogram description of the element
    :ivar arcs_of_circle: Description of the element contour by a set of
        arcs of circle. For each of these, the position of the start
        point is given together with the curvature radius. The end point
        is given by the start point of the next arc of circle.
    :ivar annulus: The element is an annulus of centre R, Z, with inner
        radius radius_inner and outer radius radius_outer
    :ivar thick_line: The element is approximated by a rectangle defined
        by a central segment and a thickness in the direction
        perpendicular to the segment
    """
    class Meta:
        name = "outline_2d_geometry_static"

    geometry_type: int = field(
        default=999999999
    )
    outline: Optional[Rz1DStatic] = field(
        default=None
    )
    rectangle: Optional[RectangleStatic] = field(
        default=None
    )
    oblique: Optional[ObliqueStatic] = field(
        default=None
    )
    arcs_of_circle: Optional[ArcsOfCircleStatic] = field(
        default=None
    )
    annulus: Optional[AnnulusStatic] = field(
        default=None
    )
    thick_line: Optional[ThickLineStatic] = field(
        default=None
    )


@dataclass
class PfCoilsElements(IdsBaseClass):
    """
    Each PF coil is comprised of a number of cross-section elements described
    individually.

    :ivar name: Name of this element
    :ivar identifier: Identifier of this element
    :ivar turns_with_sign: Number of effective turns in the element for
        calculating magnetic fields of the coil/loop; includes the sign
        of the number of turns (positive means current is counter-
        clockwise when seen from above)
    :ivar area: Cross-sectional areas of the element
    :ivar geometry: Cross-sectional shape of the element
    """
    class Meta:
        name = "pf_coils_elements"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    turns_with_sign: float = field(
        default=9e+40
    )
    area: float = field(
        default=9e+40
    )
    geometry: Optional[Outline2DGeometryStatic] = field(
        default=None
    )


@dataclass
class PfPassiveLoops(IdsBaseClass):
    """
    Passive axisymmetric conductor description in the form of non-connected loops;
    any connected loops are expressed as active coil circuits with no power supply
    attached.

    :ivar name: Name of the loop
    :ivar resistance: Passive loop resistance
    :ivar resistivity: Passive loop resistivity
    :ivar element: Each loop is comprised of a number of cross-section
        elements described  individually
    :ivar current: Passive loop current
    :ivar time: Timebase for the dynamic nodes of this loop located at
        this level of the IDS structure
    """
    class Meta:
        name = "pf_passive_loops"

    name: str = field(
        default=""
    )
    resistance: float = field(
        default=9e+40
    )
    resistivity: float = field(
        default=9e+40
    )
    element: list[PfCoilsElements] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    current: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    time: Optional[str] = field(
        default=None
    )


@dataclass
class PfPassive(IdsBaseClass):
    """
    Description of the axisymmetric passive conductors, currents flowing in them.

    :ivar ids_properties:
    :ivar loop: Passive axisymmetric conductor description in the form
        of non-connected loops; any connected loops are expressed as
        active coil circuits with no power supply attached.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "pf_passive"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    loop: list[PfPassiveLoops] = field(
        default_factory=list,
        metadata={
            "max_occurs": 500,
        }
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
