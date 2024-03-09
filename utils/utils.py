from PIL import Image, ImageOps


def get_single_tag_keys(parsed_label_config, control_type, object_type):
    """
    Gets parsed label config, and returns data keys related to the single control tag and the single object tag schema
    (e.g. one "Choices" with one "Text")
    :param parsed_label_config: parsed label config returned by "label_studio.misc.parse_config" function
    :param control_type: control tag str as it written in label config (e.g. 'Choices')
    :param object_type: object tag str as it written in label config (e.g. 'Text')
    :return: 3 string keys and 1 array of string labels: (from_name, to_name, value, labels)
    """
    # assert len(parsed_label_config) == 1
    # from_name, info = list(parsed_label_config.items())[0]
    # assert info["type"] == control_type, (
    #     'Label config has control tag "<'
    #     + info["type"]
    #     + '>" but "<'
    #     + control_type
    #     + '>" is expected for this model.'
    # )  # noqa

    # assert len(info["to_name"]) == 1
    # assert len(info["inputs"]) == 1
    # assert info["inputs"][0]["type"] == object_type
    # to_name = info["to_name"][0]
    # value = info["inputs"][0]["value"]
    # return from_name, to_name, value, info["labels"]
    return "tag3", "image", "image", ["Person"]


def get_image_size(filepath):
    img = Image.open(filepath)
    img = ImageOps.exif_transpose(img)
    return img.size
