from abc import ABC, abstractmethod

from pyannotator.antypes import (
    AnnotationInfo,
    DatasetInfo,
    EntityInfo,
    ImageInfo,
    ProjectInfo,
)


class IAnnotationBackend(ABC):
    """Interface for annotation tools.

    This abstract base class defines the interface for annotation tools that can be used
    to create annotation projects and upload images for labeling.

    Attributes:
        name (str): Name of the annotation tool

    Methods:
        create_project(name, description, classes): Creates a new annotation project
        upload_image(): Uploads an image to the annotation tool
    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def create_project(self, kwargs) -> ProjectInfo:
        pass

    @abstractmethod
    def update_project(self, kwargs) -> ProjectInfo:
        pass

    @abstractmethod
    def list_projects(self, kwargs) -> list[ProjectInfo]:
        pass

    @abstractmethod
    def get_project(self, kwargs) -> ProjectInfo:
        pass

    @abstractmethod
    def delete_project(self, kwargs) -> None:
        pass

    @abstractmethod
    def create_dataset(self, kwargs) -> DatasetInfo:
        pass

    @abstractmethod
    def update_dataset(self, kwargs) -> DatasetInfo:
        pass

    @abstractmethod
    def list_datasets(self, kwargs) -> list[DatasetInfo]:
        pass

    @abstractmethod
    def get_dataset(self, kwargs) -> DatasetInfo:
        pass

    @abstractmethod
    def delete_dataset(self, kwargs) -> None:
        pass

    @abstractmethod
    def upload_image(self, kwargs) -> ImageInfo:
        pass

    @abstractmethod
    def upload_images(self, kwargs) -> list[ImageInfo]:
        pass

    @abstractmethod
    def create_entity(self, kwargs) -> AnnotationInfo:
        pass

    @abstractmethod
    def create_entities(self, kwargs) -> list[EntityInfo]:
        pass

    @abstractmethod
    def create_annotation(self, kwargs) -> AnnotationInfo:
        pass

    @abstractmethod
    def upload_annotation(self, kwargs) -> None:
        pass

    @abstractmethod
    def list_annotations(self, kwargs) -> list[AnnotationInfo]:
        pass

    @abstractmethod
    def download_annotations(self, kwargs) -> list[AnnotationInfo]:
        pass
