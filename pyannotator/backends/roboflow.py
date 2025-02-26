from pyannotator.interfaces import IAnnotationBackend


class RoboFlowBackend(IAnnotationBackend):
    def __init__(self):
        super().__init__("roboflow")

    def create_project(self, name, description, classes):
        pass

    def upload_image():
        pass
