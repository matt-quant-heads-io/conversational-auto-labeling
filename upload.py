import datetime
import os
import pathlib

import constants

PATH_TO_FRAMES = str(pathlib.Path(__file__).parent.resolve()) + "/data/images"
LABEL_STUDIO_PROJECT_ID = 1


def sample_imgs_to_upload(verbose=False):
    img_paths = []
    num_imgs = 0
    for f in os.listdir(PATH_TO_FRAMES):
        if ".jpeg" in f:
            img_paths.append(f"{PATH_TO_FRAMES}/{f}")
            num_imgs += 1

    if verbose:
        print(f"Total images: {num_imgs}")

    return img_paths


def exec_curl_cmd_to_upload_frame(abs_path_to_img_frame):
    curl_upload_cmd = f"curl -H 'Authorization: Token {constants.LABEL_STUDIO_ACCESS_TOKEN}' -X POST \
         '{constants.LABEL_STUDIO_HOST}projects/{LABEL_STUDIO_PROJECT_ID}/import' -F 'file=@{abs_path_to_img_frame}'"

    exit_code = os.system(curl_upload_cmd)
    if exit_code != 0:
        print(
            f"Returned error code {exit_code} after trying to upload img frame {abs_path_to_img_frame}"
        )


def run(verbose=False):
    sampled_frames_to_upload = sample_imgs_to_upload()

    start_time = datetime.datetime.now()

    num_files_uploaded = 0
    for sampled_frame in sampled_frames_to_upload:
        num_files_uploaded += 1
        exec_curl_cmd_to_upload_frame(sampled_frame)

    end_time = datetime.datetime.now()

    if verbose:
        upload_time = (end_time - start_time).total_seconds()
        print(f"It took {upload_time} seconds to upload {num_files_uploaded} img files")


if __name__ == "__main__":
    run(verbose=True)
