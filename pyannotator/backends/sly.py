import logging
from typing import Any

import requests
import supervisely as sly
from numpy import ndarray

from pyannotator.antypes import (
    AnnotationInfo,
    AnnotatorInfo,
    DatasetInfo,
    GeometryType,
    ImageInfo,
    LabelClassInfo,
    LabelInfo,
    ProjectInfo,
    ProjectType,
)
from pyannotator.interfaces import IAnnotationBackend


class SlyClass(sly.ObjClass):
    """
    Entity class information adapter for sly.

    Example:
    --------
    .. code-block:: python
        sly_class = SlyClass(entity_info=EntityClassInfo(name="claim_id"))
    """

    geometry_type_mapping = {
        GeometryType.POLYGON: sly.Polygon,
        GeometryType.BITMAP: sly.Bitmap,
        GeometryType.BBOX: sly.Rectangle,
        GeometryType.POINT: sly.Point,
        GeometryType.POLYLINE: sly.Polyline,
    }

    def __init__(self, entity_info: LabelClassInfo):
        super().__init__(
            name=entity_info.name,
            geometry_type=self.geometry_type_mapping[entity_info.geometry_type],
            color=entity_info.color,
        )


class SlyImage(sly.ImageInfo):
    """
    Image information adapter for sly.

    Example:
    --------
    .. code-block:: python
        sly_image = SlyImage(image_info=ImageInfo(id=1, name="image.jpg", url="http://...", height=800, width=600)
    """

    def __init__(self, image_info: ImageInfo):
        super().__init__(
            id=image_info.id,
            name=image_info.name,
            full_storage_url=image_info.url,
            height=image_info.height,
            width=image_info.width,
            meta=image_info.meta or {},
        )


class SlyProject(sly.ProjectInfo):
    """
    Project information adapter for sly.

    Example:
    --------
    > sly_project = SlyProject(project_info=ProjectInfo(id=1, name="Project A", type="detection"))
    """

    def __init__(self, project_info: ProjectInfo):
        super().__init__(
            name=project_info.name,
            description=project_info.description or "",
            type=project_info.type,
            meta=project_info.meta or {},
        )


class SlyAnnotation(sly.Annotation):
    """
    Annotation information adapter for sly.

    Example:
    --------
    > sly_annotation = SlyAnnotation(annotation_info=AnnotationInfo(id=1, image_id=5, entity_infos_ids=[10, 20]))
    """

    def __init__(self, annotation_info: AnnotationInfo, entities: list[sly.Label]):
        super().__init__(
            image_id=annotation_info.image_id,
            labels=entities,  # Convert entity IDs to sly Labels separately
            meta=annotation_info.meta or {},
        )


class SlyEntity(sly.Label):
    """
    Entity information adapter for sly.

    Example:
    --------
    > sly_entity = SlyEntity(entity_info=EntityInfo(id=1, class_id=10, geometry=[(0,0), (10,10)]))
    """

    def __init__(self, entity_info: LabelInfo, obj_class: sly.ObjClass):
        geometry = sly.Polygon(
            entity_info.geometry
        )  # Adjust geometry conversion as needed
        super().__init__(
            obj_class=obj_class,
            geometry=geometry,
            tags=[],  # Add tag support if needed
            meta=entity_info.meta or {},
        )


class SlyBackend(IAnnotationBackend):
    """
    Backend implementation for Supervisely annotation platform.

    :param token: API token for authentication with Supervisely
    :type token: str

    The SlyBackend class provides methods to:
    - Create and manage projects
    - Upload images
    - Create annotations
    - Manage entity classes
    - Interface with the Supervisely API
    """

    project_type_mapping = {
        ProjectType.IMAGES: sly.ProjectType.IMAGES,
        ProjectType.VIDEOS: sly.ProjectType.VIDEOS,
        ProjectType.VOLUMES: sly.ProjectType.VOLUMES,
    }

    geometry_type_mapping = {
        GeometryType.BBOX: sly.Rectangle,
        GeometryType.POLYGON: sly.Polygon,
        GeometryType.POLYLINE: sly.Polyline,
        GeometryType.POINT: sly.Point,
    }

    def __init__(self, token):
        self.token = token
        self.api: sly.Api = sly.Api(
            server_address="https://app.supervise.ly",
            token=token,
        )

        self.workspace: sly.WorkspaceInfo = self._get_current_ws()
        self.current_project_id: int | None = None
        self.current_dataset_id: int | None = None
        self.user: AnnotationInfo | None = self._get_user()
        self.objectClassCollection: sly.ObjClassCollection | None = None
        self.logger = self._config_logger()

        self.logger.info(f"Logged in as user: {self.user.email}")

    def _config_logger(self):
        """
        Configure logger.

        :return: logger object
        """
        logger = logging.getLogger("SlyBackend")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(name)s] [%(levelname)s] %(asctime)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def _get_current_ws(self) -> sly.WorkspaceInfo:
        """Retrieve the current workspace in sly."""
        team = self.api.team.get_list()[0]
        return self.api.workspace.get_list(team.id)[0]

    def _get_user(self) -> AnnotatorInfo:
        """
        Get the current user.

        :return: Logged in user information
        """
        res = requests.get(
            url="https://app.supervisely.com/public/api/v3/users.me",
            headers={"x-api-key": self.token},
            timeout=5,
        )
        return AnnotatorInfo(meta={}, **res.json()) if res.status_code == 200 else None

    def create_dataset(
        self,
        project_id: int,
        name: str,
        description: str = "",
    ) -> DatasetInfo:
        """
        Upload a dataset to sly.

        :param project_id: sly project id
        :param project_id: int
        :param name: a name for the dataset, defaults to a random name
        :type name: str
        :param description: a description for the dataset, defaults to defaults to an empty str
        :type description: str

        :return: a dataset info object
        rtype: DatasetInfo
        """
        dataset_info: sly.DatasetInfo = self.api.dataset.create(
            project_id=project_id,
            name=name,
            description=description,
            change_name_if_conflict=True,
        )

        return DatasetInfo(
            id=dataset_info.id,
            name=dataset_info.name,
            description=dataset_info.description,
            meta={
                "project_id": project_id,
            },
            created_at=dataset_info.created_at,
            updated_at=dataset_info.updated_at,
        )

    def update_dataset(
        self,
        dataset_id: int,
        name: str,
        description: str = "",
    ) -> None:
        """
        Update a dataset in sly.

        :param kwargs: keyword arguments for dataset update
        :return: updated dataset info object
        :rtype: DatasetInfo
        """
        self.api.dataset.update(dataset_id, name=name, description=description)

    def list_datasets(self, proj_id: int) -> list[DatasetInfo]:
        """
        List all datasets in a project.

        :param proj_id: project id
        :type proj_id: int

        :return: list of dataset info objects
        :rtype: list[DatasetInfo]
        """
        datasets: list[sly.DatasetInfo] = self.api.dataset.get_list(proj_id)
        return [
            DatasetInfo(
                id=dataset.id,
                name=dataset.name,
                description=dataset.description,
                meta={
                    "project_id": proj_id,
                },
                created_at=dataset.created_at,
                updated_at=dataset.updated_at,
            )
            for dataset in datasets
        ]

    def list_all_datasets(self) -> list[DatasetInfo]:
        """
        List all datasets in the workspace.

        :return: list of dataset info objects
        :rtype: list[DatasetInfo]
        """
        datasets: dict = self.api.dataset.get_list_all()
        datasets_entities: list[sly.DatasetInfo] = datasets.get("entities", [])
        return [
            DatasetInfo(
                id=dataset.id,
                name=dataset.name,
                description=dataset.description,
                meta={
                    "project_id": dataset.project_id,
                },
                created_at=dataset.created_at,
                updated_at=dataset.updated_at,
            )
            for dataset in datasets_entities
        ]

    def get_dataset(self, dataset_id: int) -> DatasetInfo:
        """
        Get dataset information by id.

        :param dataset_id: dataset id
        :type dataset_id: int

        :return: dataset info object
        :rtype: DatasetInfo
        """
        dataset_info: sly.DatasetInfo = self.api.dataset.get_info_by_id(dataset_id)

        return DatasetInfo(
            id=dataset_info.id,
            name=dataset_info.name,
            description=dataset_info.description,
            meta={
                "project_id": dataset_info.project_id,
            },
            created_at=dataset_info.created_at,
            updated_at=dataset_info.updated_at,
        )

    def delete_dataset(self, dataset_id) -> None:
        """
        Delete a dataset in sly.

        :param dataset_id: dataset id
        :type dataset_id: int
        """
        self.api.dataset.remove(dataset_id)

    def create_project(
        self,
        name: str,
        description: str = "",
        project_type: ProjectType = ProjectType.IMAGES,
        classes: list[dict[str, Any]] | None = None,
        tags: list[sly.TagMeta] | None = None,
    ) -> ProjectInfo:
        """
        Create a new project in sly.

        :param name: a name for the project
        :type name: str
        :param description: a description for the project, defaults to an empty str
        :type description: str
        :param project_type: the type of the project, defaults to ``ProjectType.IMAGES``
        :type project_type: ProjectType
        :param classes: a list of entity classes, defaults to ``None``
        :type classes: list[EntityClassInfo]
        :param tags: a list of tags, defaults to ``None``
        :type tags: list[sly.TagMeta]
        > The project info meta contains the following data:
            - classes

        :return: a project info object
        :rtype: ProjectInfo
        """
        proj = self.api.project.create(
            workspace_id=self.workspace.id,
            name=name,
            description=description,
            type=self.project_type_mapping[project_type],
            change_name_if_conflict=True,
        )

        self.api.project.update_meta(
            id=proj.id,
            meta=sly.ProjectMeta(
                obj_classes=self._create_class_obj_collection(classes),
                tag_metas=tags,
                project_settings=None,
            ),
        )
        dataset = self.create_dataset(project_id=proj.id, name=name, description="")

        self.logger.info(f"Created new project [{proj.name}] [id = {proj.id}] ")

        self.current_project_id = proj.id

        return ProjectInfo(
            id=proj.id,
            name=proj.name,
            description=proj.description,
            type=proj.type,
            meta={
                "classes": classes,
            },
            created_at=proj.created_at,
            updated_at=proj.updated_at,
        )

    def get_project(self, proj_id) -> ProjectInfo:
        """
        Get project information.

        :param id: project id
        :return: project information
        """
        proj = self.api.project.get_info_by_id(proj_id)
        return ProjectInfo(
            id=proj.id,
            name=proj.name,
            description=proj.description,
            type=proj.type,
            meta={
                "classes": None,
                "images": None,
            },
            created_at=proj.created_at,
            updated_at=proj.updated_at,
        )

    def update_project(
        self,
        project_id: int,
        name: str = None,
        description: str = None,
        classes: list[dict[str, Any]] = None,
        project_type: ProjectType = ProjectType.IMAGES,
        tags: list[sly.TagMeta] = None,
    ) -> ProjectInfo:
        """
        Update project metadata.

        :param project_id: Project ID
        :param kwargs: Keyword arguments with project metadata

        :return: None
        """
        self.api.project.update(
            id=project_id,
            name=name,
            description=description,
        )

        if classes or tags or project_type:
            meta: sly.ProjectMeta = self.api.project.update_meta(
                id=project_id,
                meta=sly.ProjectMeta(
                    obj_classes=self._create_class_obj_collection(classes),
                    tag_metas=tags,
                    project_type=project_type,
                    project_settings=None,
                ),
            )
            self.logger.info(
                f"Updated project [{project_id}] metadata: {meta.to_json()}"
            )

        return ProjectInfo(
            id=project_id,
            name=name,
            description=description,
            type=project_type,
            meta={
                "classes": classes,
                "images": None,
            },
        )

    def list_projects(self, kwargs) -> list[ProjectInfo]:
        """
        list all projects available in sly.

        :return: list of :py:class:`sly.ProjectInfo` objects
        """
        projects_list = self.api.project.get_list_all()["entities"]

        return [
            ProjectInfo(
                id=proj.id,
                name=proj.name,
                description=proj.description,
                type=proj.type,
                created_at=proj.created_at,
                updated_at=proj.updated_at,
            )
            for proj in projects_list
        ]

    def delete_project(self, proj_id):
        return self.api.project.remove(proj_id)

    def upload_image(
        self,
        *,
        dataset_id: int,
        name: str,
        path: str = None,
        link: str = None,
        np: ndarray = None,
    ) -> ImageInfo:
        if not (path or link or np):
            raise ValueError("Either path, link or np must be provided")

        image_info = None
        if path:
            image_info = self.api.image.upload_path(dataset_id, name, path)
        elif link:
            image_info = self.api.image.upload_link(dataset_id, name, link)
        else:
            image_info = self.api.image.upload_np(dataset_id, name, np)

        return ImageInfo(
            id=image_info.id,
            name=image_info.name,
            url=image_info.link,
            height=image_info.height,
            width=image_info.width,
            meta=image_info.meta,
            created_at=image_info.created_at,
            updated_at=image_info.updated_at,
        )

    def upload_images(
        self,
        *,
        dataset_id: int,
        names: list[str],
        paths: list[str] = None,
        links: list[str] = None,
        ndarrays: list[ndarray] = None,
    ) -> list[ImageInfo]:
        if not (paths or links or ndarrays):
            raise ValueError("Either paths, links or np must be provided")

        images = []
        if paths:
            images = self.api.image.upload_paths(dataset_id, names, paths)
        elif links:
            images = self.api.image.upload_links(dataset_id, names, links)
        else:
            images = self.api.image.upload_nps(dataset_id, names, ndarrays)

        return [
            ImageInfo(
                id=image.id,
                name=image.name,
                url=image.full_storage_url,
                height=image.height,
                width=image.width,
                meta=image.meta,
                created_at=image.created_at,
                updated_at=image.updated_at,
            )
            for image in images
        ]

    def create_entity(
        self,
        geometry: list[int],
        obj_class: dict[str, Any],
        text: str | None = None,
        tags: list[str] | None = None,
    ) -> LabelInfo:
        return LabelInfo()

    def create_entities(self, kwargs) -> list[LabelInfo]:
        pass

    def download_annotation(self, img_id):
        pass

    def download_annotations(self, dataset_id):
        pass

    @classmethod
    def create_classes(
        cls, classes: list[dict[str, str | list[int] | GeometryType]]
    ) -> list[dict]:
        """

        example:
        ```
        > clss = SlyBackend.create_classes(
            [
                {"id": 0, "name": "claim_id"},
                {"id": 1, "name": "name"},
                {"id": 2, "name": "medical_id"},
                {"id": 3, "name": "medical_provider_name"},
                {"id": 4, "name": "employer_name"},
                {"id": 5, "name": "medical_information"},
                {"id": 6, "name": "date"},
                {"id": 7, "name": "signature"},
                {"id": 8, "name": "stamp"},
                {"id": 9, "name": "diagnosis"},
                {"id": 10, "name": "drug"},
                {"id": 11, "name": "test"},
                {"id": 12, "name": "instructions"},
                {"id": 13, "name": "national_id"},
                {"id": 14, "name": "mobile_number"},
                {"id": 15, "name": "drug_instruction"},
            ]
        )
        ```
        """
        return [
            LabelClassInfo(
                id=_cls.get("id"),
                name=_cls.get("name"),
                color=_cls.get("color"),
                geometry_type=_cls.get("geometry_type", GeometryType.BBOX),
                meta=_cls.get("meta"),
            )
            for _cls in classes
        ]

    @classmethod
    def _create_class_obj_collection(
        cls, classes: list[dict[str, str | list[int] | GeometryType]]
    ) -> sly.ObjClassCollection:
        """
        Initialize a list of class objects.

        :param classes: list of classes, each element should be a dictionary \
            containing ``name``, ``color``, ``geometry_type``
        :return: list of class objects
        """

        return sly.ObjClassCollection(
            [
                sly.ObjClass(
                    name=_cls.get("name"),
                    color=_cls.get("color"),
                    geometry_type=cls.geometry_type_mapping[
                        _cls.get(
                            "geometry_type",
                            _cls.get("geometry_type", GeometryType.BBOX),
                        )
                    ],
                )
                for _cls in classes
            ]
        )

    @classmethod
    def _create_label_obj(
        cls,
        geometry: list[tuple[int | float, int | float]],
        obj_class: LabelClassInfo,
        description: str = None,
        tags=None,
    ) -> sly.Label:
        """
        Initialize a label object.

        :param geometry: geometry of the label
        :param obj_class: object class of the label
        :param description: description of the label (text inside the crop)
        :param tags: tags of the label

        :return: a new label `py:class:`sly.Label` object
        """
        return sly.Label(
            geometry=geometry,
            obj_class=obj_class,
            description=description,
            tags=tags,
        )

    @classmethod
    def _create_label_objs(
        cls, labels: list[dict[str, str | list[int] | GeometryType]]
    ) -> list[sly.Label]:
        """
        Initialize a list of label objects.

        :param labels: list of labels, each element should be a dictionary \
            containing ``geometry``, ``obj_class``, ``description``, ``tags``
        :return: list of label objects
        """
        return [
            sly.Label(
                geometry=label.get("geometry", None),
                obj_class=label.get("obj_class", None),
                description=label.get("description", None),
                tags=label.get("tags", None),
            )
            for label in labels
        ]

    @classmethod
    def _create_annotation_obj(
        cls, img_info: sly.ImageInfo | dict[str, int], labels: list[sly.Label]
    ):
        if isinstance(img_info, dict):
            return sly.Annotation(
                image_id=img_info["id"],
                img_size=(img_info["height"], img_info["width"]),
                img_tags=img_info.get("tags", None),
                labels=labels,
            )

        return sly.Annotation(
            image_id=img_info.id,
            img_size=(img_info.height, img_info.width),
            img_tags=img_info.tags,
            labels=labels,
        )

    @classmethod
    def _create_annotation_objs(
        cls, img_infos: list[sly.ImageInfo], labels: list[list[sly.Label]]
    ) -> list[sly.Annotation]:
        """
        Initialize a list of annotation objects.

        :param img_infos: list of image infos
        :param labels: list of labels, each element should be a list of labels
        :return: list of annotation objects
        """
        return [
            sly.Annotation(
                image_id=img_info.id,
                img_size=(img_info.height, img_info.width),
                labels=labels[i],
                img_tags=img_info.tags,
            )
            for i, img_info in enumerate(img_infos)
        ]
