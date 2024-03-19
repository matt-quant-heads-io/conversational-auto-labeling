import io
import json
import pathlib

import cv2
from label_studio_ml.model import LabelStudioMLBase
from ultralytics import YOLO, YOLOWorld

import constants
import utils.utils as utils

PROJECT_ROOT_PATH = str(pathlib.Path(__file__).parent.parent.resolve())


def json_load(file, int_keys=False):
    """
    Description of json_load

    Args:
        file (undefined):
        int_keys=False (undefined):

    """
    with io.open(file, encoding="utf8") as f:
        data = json.load(f)
        if int_keys:
            return {int(k): v for k, v in data.items()}

        return data


class DetectionAnnotator(LabelStudioMLBase):
    """
    Description of DetectionAnnotator

    Attributes:
        checkpoint_file (type):
        labels_file (type):
        image_path (type):

    Inheritance:
        LabelStudioMLBase:

    Args:
        score_threshold=0.01 (undefined):
        device="cpu" (undefined):
        **kwargs (undefined):

    """

    def __init__(
        self,
        score_threshold=0.5,
        **kwargs,
    ):
        super(DetectionAnnotator, self).__init__(**kwargs)
        # TODO: Refactor this into a different model wrapper
        # self.checkpoint_file = (
        #     str(pathlib.Path(__file__).parent.resolve()) + "/models/yolov8x.pt"
        # )
        # self.model = YOLO(self.checkpoint_file)
        self.checkpoint_file = (
            str(pathlib.Path(__file__).parent.resolve()) + "/models/yolov8s-world.pt"
        )
        self.model = YOLOWorld(self.checkpoint_file)

        self.image_path = f"{PROJECT_ROOT_PATH}/data/images"
        self.labels_file = "labels_config.json"
        self.parsed_label_config = kwargs.get("labels_conf") or json_load(
            f"{PROJECT_ROOT_PATH}/configs/{self.labels_file}"
        )

        (
            self.from_name,
            self.to_name,
            self.value,
            self.label_map,
        ) = utils.get_single_tag_keys(self.parsed_label_config)
        self.score_thresh = score_threshold

    def predict(self, tasks, **kwargs):
        """
        Description of predict

        Args:
            self (undefined):
            tasks (undefined):
            **kwargs (undefined):

        """
        predictions = []
        for task in tasks:
            prediction = self.predict_one_task(task)
            predictions.append(prediction)
        return predictions

    def predict_one_task(self, task):
        """
        Description of predict_one_task

        Args:
            self (undefined):
            task (undefined):

        """
        print(f"task: {task}")
        task_id, local_img_path = task["id"], task["data"]["image"]
        image_path = local_img_path.replace(
            "data", constants.LABEL_STUDIO_PATH_TO_MEDIA_FOLDER
        )

        results = []
        all_scores = []
        img_width, img_height = utils.get_image_size(image_path)
        model_results = self.model(cv2.imread(image_path))[0]
        for model_result in model_results:
            pred = json.loads(model_result.tojson())
            for bbox in pred:
                if not bbox:
                    continue

                if bbox["confidence"] < self.score_thresh:
                    continue

                output_label = self.label_map.get(bbox["name"])
                if not output_label:
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


# pdo = DetectionAnnotator()
# create_annotations_from_prediction(constants.PROJECT_NAME)
