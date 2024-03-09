import io
import json
import logging
import os
import pathlib
import urllib.request
import uuid

import cv2
from label_studio_ml.model import LabelStudioMLBase
from label_studio_tools.core.utils.io import get_data_dir
from ultralytics import YOLO

import constants
import utils.utils as utils

logger = logging.getLogger(__name__)


class PersonDetectionAnnotator(LabelStudioMLBase):
    def __init__(
        self,
        image_dir=None,
        score_threshold=0.01,
        device="cpu",
        **kwargs,
    ):
        super(PersonDetectionAnnotator, self).__init__(**kwargs)
        self.checkpoint_file = (
            str(pathlib.Path(__file__).parent.resolve()) + "/models/yolov8x.pt"
        )
        self.labels_file = "labels_config.json"
        self.image_path = (
            str(pathlib.Path(__file__).parent.parent.resolve()) + "/data/images"
        )

        # default Label Studio image upload folder
        upload_dir = os.path.join(get_data_dir(), "media", "upload")
        self.image_dir = image_dir or upload_dir
        logger.debug(f"{self.__class__.__name__} reads images from {self.image_dir}")

        self.parsed_label_config = json_load(
            f"{str(pathlib.Path(__file__).parent.parent.resolve())}/configs/{self.labels_file}"
        )
        # TODO: load this in from project req response
        self.label_map = {"Person": "Person", "person": "Person"}

        (
            self.from_name,
            self.to_name,
            self.value,
            self.labels_in_config,
        ) = utils.get_single_tag_keys(
            self.parsed_label_config, "RectangleLabels", "Image"
        )
        schema = list(self.parsed_label_config.values())[0]
        self.labels_in_config = set(self.labels_in_config)

        self.model = YOLO(self.checkpoint_file)
        self.score_thresh = score_threshold

        self.labels_attrs = schema.get("labels_attrs")
        # self.build_labels_from_labeling_config(schema)

    def predict(self, tasks, **kwargs):
        predictions = []
        for task in tasks:
            prediction = self.predict_one_task(task)
            predictions.append(prediction)
        return predictions

    def predict_one_task(self, task):
        print(f"task: {task}")
        task_id, local_img_path = task["id"], task["data"]["image"]
        image_path = local_img_path.replace(
            "data", constants.LABEL_STUDIO_PATH_TO_MEDIA_FOLDER
        )

        results = []
        all_scores = []
        img_width, img_height = utils.get_image_size(image_path)
        classes = constants.PDO_CLASSES
        model_results = self.model(cv2.imread(image_path))[0]
        for model_result in model_results:
            pred = json.loads(model_result.tojson())
            for bbox in pred:
                if not bbox:
                    # results.append({})
                    continue

                output_label = self.label_map.get(bbox["name"])
                if not output_label:
                    # results.append({})
                    continue

                if bbox["confidence"] < self.score_thresh:
                    # results.append({})
                    continue

                x, y, xmax, ymax = (
                    int(bbox["box"]["x1"]),
                    int(bbox["box"]["y1"]),
                    int(bbox["box"]["x2"]),
                    int(bbox["box"]["y2"]),
                )

                results.append(
                    {
                        "from_name": self.from_name,
                        "to_name": self.to_name,
                        "type": "rectanglelabels",
                        "value": {
                            "rectanglelabels": [output_label],
                            "x": float(x) / img_width * 100,
                            "y": float(y) / img_height * 100,
                            "width": (float(xmax) - float(x)) / img_width * 100,
                            "height": (float(ymax) - float(y)) / img_height * 100,
                        },
                        "score": bbox["confidence"],
                    }
                )
                all_scores.append(bbox["confidence"])
        avg_score = sum(all_scores) / max(len(all_scores), 1)
        print(f">>> RESULTS: {results}")
        return {
            "result": results,
            "score": avg_score,
            "model_version": "pda",
            "task_id": task_id,
        }


def json_load(file, int_keys=False):
    with io.open(file, encoding="utf8") as f:
        data = json.load(f)
        if int_keys:
            return {int(k): v for k, v in data.items()}
        else:
            return data


def get_project_info_by_name(project_name):
    req = urllib.request.Request(constants.GET_PROJECTS_HTTP_REQ)
    req.add_header("Authorization", f"Token {constants.LABEL_STUDIO_ACCESS_TOKEN}")
    print(f"req: {req}")
    projects = json.loads(
        urllib.request.urlopen(req).read().decode().replace("'", '"')
    ).get("results")

    print(f"projects: {projects}")

    if projects:
        for project in projects:
            if project["title"] == project_name:
                return project

    return


def get_tasks_by_project_name(project_name):
    project_info = get_project_info_by_name(project_name)
    project_id = project_info.get("id")

    tasks = []
    if project_id:
        req = urllib.request.Request(
            constants.GET_TASKS_HTTP_REQ.format(project_id=project_id)
        )
        req.add_header("Authorization", f"Token {constants.LABEL_STUDIO_ACCESS_TOKEN}")
        tasks = json.loads(
            urllib.request.urlopen(req).read().decode().replace("'", '"')
        )

    return tasks


def create_annotations_from_prediction(pda, project_name):
    project_info = get_project_info_by_name(project_name)
    project_id = project_info["id"]
    tasks_info = get_tasks_by_project_name(project_name)

    for task_info in tasks_info:
        result_info = pda.predict_one_task(task_info)
        print(f"task_info: {task_info}")
        task_id, results = result_info["task_id"], result_info["result"]

        post_req_body = {
            "completed_by": 1,  # TODO: refactor this via adding method to get user - http://api.labelstud.io/api/current-user/whoami
            "unique_id": str(uuid.uuid1()),
            "result": results,
            "was_cancelled": False,
            "ground_truth": True,
            "draft_created_at": None,
            "lead_time": 0,
            "import_id": 0,  # TODO: refactor this to use the actual value?
            "last_action": None,
            "task": task_id,
            "project": project_id,
            "updated_by": 1,
            "parent_prediction": None,
            "parent_annotation": None,
            "last_created_by": 1,
        }
        post_req_body = str(json.dumps(post_req_body)).encode("utf-8")

        # TODO: Refactor this to use a persistent connection (avoid connection drop error error on LS side)
        post_req = urllib.request.Request(
            constants.CREATE_ANNOTATION_HTTP_REQ.format(task_id=task_id),
            data=post_req_body,
        )
        post_req.add_header(
            "Authorization", f"Token {constants.LABEL_STUDIO_ACCESS_TOKEN}"
        )
        post_req.add_header("Content-Type", "application/json")
        resp = json.loads(
            urllib.request.urlopen(post_req).read().decode("utf-8").replace("'", '"')
        )

        if resp:
            print(f"[POST REQUEST> Created annotations]: {resp}")


# pdo = PersonDetectionAnnotator()
# create_annotations_from_prediction(constants.PROJECT_NAME)
