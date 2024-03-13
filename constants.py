import pathlib

LABEL_STUDIO_HOST = "http://127.0.0.1:8080/api/"
LABEL_STUDIO_ACCESS_TOKEN = "ENTER_YOUR_LABEL_STUDIO_ACCOUNT_KEY"
LABEL_STUDIO_PATH_TO_MEDIA_FOLDER = (
    "/path/to/label-studio/project/root/label_studio/media/"
)
PROJECT_ID = 1
GET_ANNOTATIONS_HTTP_REQ = LABEL_STUDIO_HOST + "tasks/{task_id}/annotations/"
PROJECT_NAME = "automated annotation 1"
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
