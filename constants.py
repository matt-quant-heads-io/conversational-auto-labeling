import pathlib

LABEL_STUDIO_HOST = "http://127.0.0.1:8080/api/"  # "http://0.0.0.0:8080/api/"
LABEL_STUDIO_ACCESS_TOKEN = "52cd6164136038a0b386bc8d90f7b5c4cbda594e"  # "a8014933de909f8e8bc2463cef92a04995b806e3"
LABEL_STUDIO_PATH_TO_MEDIA_FOLDER = (
    "/Users/matt/as-auto-data-annotation/label-studio/media/"
)
PROJECT_ID = 1
GET_ANNOTATIONS_HTTP_REQ = LABEL_STUDIO_HOST + "tasks/{task_id}/annotations/"
PROJECT_NAME = "automated annotation 1"  # "Art Sentry Person Detection Oracle"
GET_PROJECTS_HTTP_REQ = LABEL_STUDIO_HOST + "projects/"
GET_TASKS_HTTP_REQ = LABEL_STUDIO_HOST + "projects/{project_id}/tasks/"
CREATE_ANNOTATION_HTTP_REQ = LABEL_STUDIO_HOST + "tasks/{task_id}/annotations/"
CHECKPOINT_FILE_ABS_PATH = "models/yolov8x.pt"
LOCAL_IMG_PATH_PREFIX = str(pathlib.Path(__file__).parent.resolve()) + "/data"
LOCAL_TO_ABS_IMAGE_PATH_PREFIX_MAP = {
    "data": str(pathlib.Path(__file__).parent.resolve()) + "/data/images"
}
LOCAL_IMG_PATH_FOR_PROJECT_ROOT = LOCAL_IMG_PATH_PREFIX + "/{project_id}"
DATA_UNDEFINED_NAME = "$undefined$"

# TODO: Read this in from config
PDO_CLASSES = ["Person"]
