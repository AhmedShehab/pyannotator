from enum import Enum
from typing import Any

from numpy import ndarray

from pyannotator.antypes import DatasetInfo, ProjectInfo, ProjectType
from pyannotator.backends import SlyBackend


class AnnotationBackend(Enum):
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
        backend = Annotationbackend(backend=AnnotationBackends.SUPERVISELY)
        backend.create_project("my_project", "Project description", ["car", "person"])
    """

    def __init__(self, backend, token):
        self.client = self._create_annotation_backend(backend, token)

    def _create_annotation_backend(self, backend: AnnotationBackend, token):
        if not isinstance(backend, AnnotationBackend):
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

    def create_dataset(
        self,
        project_id: int,
        name: str,
        description: str = "",
    ) -> DatasetInfo:
        return self.client.create_dataset(project_id, name, description)

    def update_dataset(
        self,
        dataset_id: int,
        name: str,
        description: str = "",
    ) -> None:
        self.client.update_dataset(dataset_id, name, description)

    def list_datasets(self, proj_id: int) -> list[DatasetInfo]:
        return self.client.list_datasets(proj_id)

    def list_all_datasets(self) -> list[DatasetInfo]:
        return self.client.list_all_datasets()

    def get_dataset(self, dataset_id: int) -> DatasetInfo:
        return self.client.get_dataset(dataset_id)

    def delete_dataset(self, dataset_id) -> None:
        self.client.delete_dataset(dataset_id)
