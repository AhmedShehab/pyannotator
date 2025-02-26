from abc import ABC, abstractmethod


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
    def create_project(self, kwargs):
        pass

    @abstractmethod
    def upload_image(self, kwargs):
        pass

    @abstractmethod
    def update_project(self, kwargs):
        pass

    @abstractmethod
    def delete_project(self, kwargs):
        pass

    @abstractmethod
    def download_annotations(self, kwargs):
        pass
