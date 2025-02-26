from typing import Any
from enum import Enum
from pydantic import BaseModel as BaseInfo


class GeometryType(Enum):
    """Geometry Type enum class, it represents :mod:`supervisely.geometry` types."""

    POLYGON = 0
    BITMAP = 1  # FIXME NOT SUPPORTED YET
    BBOX = 2
    POINT = 3
    POLYLINE = 4


class ProjectType(Enum):
    """Project Type enum class, it represents :py:class:`supervisely.ProjectType`."""

    IMAGES = "images"
    VIDEOS = "videos"
    VOLUMES = "volumes"


class AnnotatorInfo(BaseInfo):
    """Annotator info on the external tool"""

    id: int
    name: str | None
    email: str | None
    meta: dict[str, Any] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ProjectInfo(BaseInfo):
    """Project info on the external tool"""

    id: int
    name: str | None
    description: str | None
    type: str
    meta: dict[str, Any] | None
    created_at: str
    updated_at: str


class ImageInfo(BaseInfo):
    """Image info on the external tool"""

    id: int
    name: str | None
    url: str
    height: int
    width: int
    meta: dict[str, Any] | None
    created_at: str
    updated_at: str


class EntityClassInfo(BaseInfo):
    """holds metadata about the annotated object class"""

    id: int | None
    name: str
    color: tuple[int, int, int]
    geometry_type: GeometryType = GeometryType.BBOX
    meta: dict[str, Any] | None


class EntityInfo(BaseInfo):
    """holds metadata about the annotated object"""

    id: int
    class_id: int | None
    text: str | None
    geometry: list[tuple[int | float, int | float]]
    created_at: str
    updated_at: str


class AnnotationInfo(BaseInfo):
    """Annotation info on the external tool"""

    id: int
    image_id: int
    entity_infos_ids: list[int] | None
    meta: dict[str, Any] | None
    created_at: str
    updated_at: str
