from typing import Any
from enum import Enum
from pydantic import BaseModel as BaseInfo
from datetime import datetime
from pyannotator.antypes import geometry


class GeometryType(Enum):
    """
    Geometry Type enum class, it represents shapely geometry types.
    """

    POLYGON = geometry.Polygon
    BITMAP = geometry.Bitmap
    BBOX = geometry.BBox
    POINT = geometry.Point
    POLYLINE = geometry.Polyline


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
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class DatasetInfo(BaseInfo):
    """Project info on the external tool"""

    id: int
    name: str | None
    description: str | None
    meta: dict[str, Any] | None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class ImageInfo(BaseInfo):
    """Image info on the external tool"""

    id: int
    name: str | None
    url: str
    height: int
    width: int
    meta: dict[str, Any] | None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class LabelClassInfo(BaseInfo):
    """holds metadata about the annotated object class"""

    id: int | None
    name: str
    color: tuple[int, int, int]
    geometry_type: GeometryType = GeometryType.BBOX
    meta: dict[str, Any] | None


class LabelInfo(BaseInfo):
    """holds metadata about the annotated object"""

    id: int
    class_id: int | None
    text: str | None
    geometry: list[tuple[int | float, int | float]]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class AnnotationInfo(BaseInfo):
    """Annotation info on the external tool"""

    id: int
    image_id: int
    entity_infos_ids: list[int] | None
    meta: dict[str, Any] | None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
