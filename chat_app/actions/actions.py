import argparse
import json
import urllib.request
import uuid

import constants
import utils.upload as upload
from annotators import ANNOTATORS_MAP

from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet


class ActionLabelDetectedObjects(Action):
    def name(self) -> Text:
        return "action_label_detected_objects"

    def run(
        self,
        dispatcher: Any,
        tracker: Any,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        upload.run()
        annotator = ANNOTATORS_MAP["detection_annotator"]()
        create_annotations_from_prediction(annotator, "automated annotation 1")

        object_type = tracker.get_slot("object_type")
        num_imgs_annotated = 3
        dispatcher.utter_message(
            text=f"Done! I uploaded {num_imgs_annotated} images and labeled all people and cars I could find :)!"
        )
        return []


def get_project_info_by_name(project_name):
    """
    Description of get_project_info_by_name

    Args:
        project_name (undefined):

    """
    req = urllib.request.Request(constants.GET_PROJECTS_HTTP_REQ)
    req.add_header("Authorization", f"Token {constants.LABEL_STUDIO_ACCESS_TOKEN}")
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
    """
    Description of get_tasks_by_project_name

    Args:
        project_name (undefined):

    """
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
    """
    Description of create_annotations_from_prediction

    Args:
        pda (undefined):
        project_name (undefined):

    """
    project_info = get_project_info_by_name(project_name)
    project_id = project_info["id"]
    tasks_info = get_tasks_by_project_name(project_name)

    for task_info in tasks_info:
        result_info = pda.predict_one_task(task_info)
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
