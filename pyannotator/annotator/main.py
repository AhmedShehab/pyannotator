from enum import Enum
from typing import Any

from numpy import ndarray

from pyannotator.antypes import DatasetInfo, ProjectInfo, ProjectType
from pyannotator.backends import SlyBackend


class AnnoationBackend(Enum):
    """Supported Backends Enum"""

    SUPERVISELY = SlyBackend
    ROBOFLOW = "roboflow"
    LABELSTUDIO = "labelstudio"


class Annotator:
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
                "The supplied backend is not valid, refer to the `AnnotationBackend`"
            )

        return backend.value(token)

    def create_project(
        self,
        *,
        name: str,
        description: str = "",
        project_type: ProjectType = ProjectType.IMAGES,
        classes: list[dict[str, Any]] | None = None,
        # tags: list[sly.TagMeta] | None = None,
    ) -> ProjectInfo:
        return self.client.create_project(
            name,
            description,
            project_type,
            classes,
        )

    def get_project(self, project_id: int) -> ProjectInfo:
        return self.client.get_project(project_id)

    def update_project(self, project_id: int, **kwargs) -> ProjectInfo:
        return self.client.update_project(project_id, **kwargs)

    def list_projects(self) -> list[ProjectInfo]:
        return self.client.list_projects()

    def delete_project(self, project_id: int):
        return self.client.delete_project(project_id)

    def create_dataset(self, project_id: int, **kwargs) -> DatasetInfo:
        return self.client.create_dataset(project_id, **kwargs)

    def get_dataset(self, dataset_id: int) -> DatasetInfo:
        return self.client.get_dataset(dataset_id)

    def list_datasets(self, project_id: int) -> list[DatasetInfo]:
        return self.client.list_datasets(project_id)

    def list_all_datasets(self) -> list[DatasetInfo]:
        return self.client.list_all_datasets()

    def update_dataset(self, dataset_id: int, **kwargs) -> DatasetInfo:
        return self.client.update_dataset(dataset_id, **kwargs)

    def delete_dataset(self, dataset_id: int):
        return self.client.delete_dataset(dataset_id)

    def upload_image(
        self,
        dataset_id: int,
        *,
        name: str,
        path: str = None,
        link: str = None,
        np: ndarray = None,
    ) -> str:
        return self.client.upload_image(dataset_id, name, path, link, np)

    def upload_images(
        self,
        dataset_id: int,
        *,
        names: list[str],
        paths: list[str] = None,
        links: list[str] = None,
        np: list[ndarray] = None,
    ) -> list[str]:
        return self.client.upload_image_batch(dataset_id, names, paths, links, np)

    def create_class(self, project_id: int, **kwargs):
        return self.client.create_class(project_id, **kwargs)

    def create_classes(self, project_id: int, **kwargs):
        return self.client.create_classes(project_id, **kwargs)

    def create_label(self, **kwargs):
        return self.client.create_label(**kwargs)

    def create_labels(self, **kwargs):
        return self.client.create_labels(**kwargs)

    def create_annotation(self, **kwargs):
        return self.client.create_annotation(**kwargs)

    def upload_annotation(self, **kwargs):
        return self.client.upload_annotation(**kwargs)

    def upload_annotations(self, **kwargs):
        return self.client.upload_annotations(**kwargs)

    def download_annotations(self, **kwargs):
        return self.client.download_annotations(**kwargs)