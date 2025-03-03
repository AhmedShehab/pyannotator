# pyannotator

An annotation management package that interacts with various external annotation tools.

## Installation

```bash
pip install pyannotator
```

## Quick Start

### Using Supervisely Backend

```python
from pyannotator import AnnotationTool, AnnotationBackend

# Initialize the annotation tool with your chosen backend
token = "YOUR_API_TOKEN"  # Get this from your annotation service
tool = AnnotationTool(
    backend=AnnotationBackend.SUPERVISELY,
    token=token
)

# Create a new project
project_info = {
    "name": "My First Project",
    "description": "A sample object detection project",
    "classes": ["car", "person", "bicycle"]
}
project = tool.create_project(**project_info)

# Upload images to your project
image_path = "path/to/your/image.jpg"
tool.upload_image(
    dataset_id = project.meta['dataset']['id'],
    name = "image.jpg",
    image_path = image_path,
)

# Download annotations
annotations = tool.download_annotations()
```

### Using Roboflow Backend

```
Coming Soon ...
```

### Using Label Studio Backend

```
Coming Soon ...
```

## Supported Backends
- **Supervisely**
- **Roboflow** -> Coming Soon ..
- **Label Studio** -> Coming Soon ..

Each backend may have specific features and requirements. Please refer to the detailed documentation for backend-specific information.

## Features
- Unified interface for multiple annotation tools
- Project creation and management
- Image upload and download
- Annotation export
- Support for various annotation types

## Documentation
For more detailed information about using pyannotator, please refer to our documentation.

## License
MIT License

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.