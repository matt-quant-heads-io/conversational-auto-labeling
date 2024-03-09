from annotators.person_detection_annotator import (
    PersonDetectionAnnotator,
    create_annotations_from_prediction,
)
import constants


def main():
    pda = PersonDetectionAnnotator()
    create_annotations_from_prediction(pda, constants.PROJECT_NAME)


if __name__ == "__main__":
    main()
