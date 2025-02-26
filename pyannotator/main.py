from enum import Enum
from typing import Any

from numpy import ndarray

from pyannotator.antypes import ProjectInfo, ProjectType
from pyannotator.backends import SlyBackend


class AnnoationBackend(Enum):
    """Supported Backends Enum"""

    SUPERVISELY = SlyBackend
    ROBOFLOW = "roboflow"
    LABELSTUDIO = "labelstudio"


class AnnotationTool:
    """
    A wrapper class for interacting with different annotation backend implementations.

    This class provides a unified interface to work with various annotation backend backends
    like Supervisely, Roboflow and Label Studio.

    Args:
        backend (str): Name of the annotation backend to use. Must be one of:
            - "supervisely": For using Supervisely annotation backend
            - "roboflow": For using Roboflow annotation backend
            - "labelstudio": For using Label Studio annotation backend

    Raises:
        ValueError: If the specified backend is not supported

    Example:
        backend = Annotationbackend(backend=AnnoationBackends.SUPERVISELY)
        backend.create_project("my_project", "Project description", ["car", "person"])
    """

    def __init__(self, backend, token):
        self.client = self._create_annotation_backend(backend, token)

    def _create_annotation_backend(self, backend: AnnoationBackend, token):
        if not isinstance(backend, AnnoationBackend):
            raise ValueError(
                "The supplied backend is not valid, please refer to the `AnnotationBackend` enum"
            )

        return backend.value(token)

    def create_project(
        self,
        *,
        name: str,
        description: str = "",
        project_type: ProjectType = ProjectType.IMAGES,
        classes: list[dict[str, Any]] | None = None,
        images: list[tuple[str, str | str | ndarray]] | None = None,
        source_type: str = None,
        # tags: list[sly.TagMeta] | None = None,
    ) -> ProjectInfo:
        return self.client.create_project(
            name,
            description,
            project_type,
            classes,
            images,
            source_type,
        )

    def delete_project(self, project_id: int):
        return self.client.delete_project(project_id)
