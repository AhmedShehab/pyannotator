from abc import ABC, abstractmethod
from typing import Any

from numpy import ndarray

from pyannotator.antypes import (
    AnnotationInfo,
    DatasetInfo,
    GeometryType,
    ImageInfo,
    LabelClassInfo,
    LabelInfo,
    ProjectInfo,
    ProjectType,
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
    def create_project(
        self,
        name: str,
        description: str,
        project_type: str,
        classes: list[dict[str, Any]] | None = None,
    ) -> ProjectInfo:
        """
        Creates a new project on the backend tool

        :param name: project's name
        :type name: str
        :param description: project's description
        :type description: str
        :param project_type: project's type, see :class:`pyannotator.antypes.ProjectType`
        :type project_type: str
        :param classes: annotation classes, defaults to None
        :type classes: list[dict[str, Any]] | None, optional
        :return: a project info container
        :rtype: ProjectInfo
        """
        pass

    @abstractmethod
    def update_project(
        self,
        project_id: str | int,
        name: str | None = None,
        description: str | None = None,
        project_type: ProjectType = None,
    ) -> ProjectInfo:
        """
        Updates a project on the backend tool

        :param project_id: project's id
        :type project_id: str | int
        :param name: project's name, defaults to None
        :type name: str | None, optional
        :param description: project's description, defaults to None
        :type description: str | None, optional
        :param project_type: project's type, defaults to None, see :class:`pyannotator.antypes.ProjectType`
        :type project_type: ProjectType, optional
        :return: a project info container
        :rtype: ProjectInfo
        """
        pass

    @abstractmethod
    def list_projects(
        self,
    ) -> list[ProjectInfo]:
        """
        list all projects on the current tool workspace

        :return: projects on the current workspace
        rtype: list[ProjectInfo]
        """
        pass

    @abstractmethod
    def get_project(self, project_id) -> ProjectInfo:
        """
        get a project on the current tool workspace

        :param project_id: project's id
        :type project_id: str | int
        :return: project info container
        :rtype: ProjectInfo
        """
        pass

    @abstractmethod
    def delete_project(self, project_id) -> None:
        """
        delete a project on the current tool workspace

        :param project_id: project's id
        :type project_id: str | int
        :return: None
        """
        pass

    @abstractmethod
    def create_dataset(
        self,
        project_id: str | int,
        name: str,
        description: str,
        geometry_type: GeometryType,
        classes: list[LabelClassInfo] | None = None,
    ) -> DatasetInfo:
        """
        Creates a new dataset on the backend tool

        :param project_id: project's id
        :type project_id: str | int
        :param name: dataset's name
        :type name: str
        :param description: dataset's description
        :type description: str
        :param geometry_type: dataset's geometry type, see :class:`pyannotator.antypes.GeometryType`
        :type geometry_type: GeometryType
        :param classes: dataset's classes, defaults to None
        :type classes: list[LabelClassInfo] | None, optional
        :return: a dataset info container
        :rtype: DatasetInfo
        """
        pass

    @abstractmethod
    def update_dataset(
        self,
        dataset_id: str | int,
        name: str | None = None,
        description: str | None = None,
        geometry_type: GeometryType = None,
    ) -> DatasetInfo:
        """
        Updates a dataset on the backend tool

        :param dataset_id: dataset's id
        :type dataset_id: str | int
        :param name: dataset's name, defaults to None
        :type name: str | None, optional
        :param description: dataset's description, defaults to None
        :type description: str | None, optional
        :param geometry_type: dataset's geometry type, defaults to None, see :class:`pyannotator.antypes.GeometryType`
        :type geometry_type: GeometryType, optional
        :return: a dataset info container
        :rtype: DatasetInfo
        """
        pass

    @abstractmethod
    def list_datasets(self, project_id) -> list[DatasetInfo]:
        """
        list all datasets on the provided project id

        :param project_id: project's id
        :type project_id: str | int
        :return: datasets on the provided project id
        rtype: list[DatasetInfo]
        """
        pass

    @abstractmethod
    def list_all_datasets(self) -> list[DatasetInfo]:
        """
        list all datasets on the current tool workspace

        :return: datasets on the current workspace
        rtype: list[DatasetInfo]
        """
        pass

    @abstractmethod
    def get_dataset(self, dataset_id) -> DatasetInfo:
        """
        get a dataset on the current tool workspace

        :param dataset_id: dataset's id
        :type dataset_id: str | int
        :return: dataset info container
        :rtype: DatasetInfo
        """
        pass

    @abstractmethod
    def delete_dataset(self, dataset_id) -> None:
        """
        delete a dataset on the current tool workspace

        :param dataset_id: dataset's id
        :type dataset_id: str | int
        :return: None
        """
        pass

    @abstractmethod
    def upload_image(self, dataset_id, name: str, source: str | ndarray) -> ImageInfo:
        """
        Uploads an image to the backend tool

        :param dataset_id: dataset's id
        :type dataset_id: str | int
        :param name: image's name
        :type name: str
        :param source: image's source, can be a path or a numpy array
        :type source: str | ndarray
        :return: image info container
        :rtype: ImageInfo
        """
        pass

    @abstractmethod
    def upload_images(
        self, dataset_id, images: list[tuple[str, str | ndarray]]
    ) -> list[ImageInfo]:
        """
        Uploads multiple images to the backend tool

        :param dataset_id: dataset's id
        :type dataset_id: str | int
        :param images: list of tuples containing image name and source
        :type images: list[tuple[str, str | ndarray]]
        :return: list of image info containers
        :rtype: list[ImageInfo]
        """
        pass

    @abstractmethod
    def create_label(self, kwargs) -> AnnotationInfo:
        pass

    @abstractmethod
    def create_labels(self, kwargs) -> list[LabelInfo]:
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
    def upload_annotations(self, kwargs) -> None:
        pass

    @abstractmethod
    def download_annotations(self, kwargs) -> list[AnnotationInfo]:
        pass
