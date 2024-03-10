from typing import Dict

from PIL import Image, ImageOps


def get_single_tag_keys(parsed_label_config: Dict):
    """
    Description of get_single_tag_keys

    Args:
        parsed_label_config (Dict):
    """
    tag = None
    from_name = None
    to_name = None
    labels = []
    for k, v in parsed_label_config.items():
        tag = k
        to_name = v.get("to_name")[0]
        from_name = v["inputs"][0]["value"]
        labels = v["labels"]

    print(f"tag: {tag}, to_name: {to_name}, from_name: {from_name}, labels: {labels}, ")
    return tag, to_name, from_name, labels


def get_image_size(filepath):
    """
    Description of get_image_size

    Args:
        filepath (str):
    """
    img = Image.open(filepath)
    img = ImageOps.exif_transpose(img)
    return img.size
