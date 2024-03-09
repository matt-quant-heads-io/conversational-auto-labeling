import os
from random import sample
import datetime
from collections import defaultdict
import json
import pathlib

import constants

# TODO: refactor all absolute paths

PATH_TO_FRAMES = str(pathlib.Path(__file__).parent.resolve()) + "/data/images"
MAX_FRAMES_PER_ROOM = 2
JSON_WRITE_PATH = str(pathlib.Path(__file__).parent.resolve())
FRAMES_UNIVERSE_FILENAME = "total_frames_universe.json"
UPLOADED_FRAMES_FILENAME = "uploaded_frames.json"
LABEL_STUDIO_PROJECT_ID = 1


def sample_frames_to_upload(
    frames_rooms_map_to_sample_from,
    write_tojson=False,
    verbose=False,
):
    uploaded_frames = defaultdict(list)
    total_sampled_frames = 0
    for k, v in frames_rooms_map_to_sample_from.items():
        num_frames_to_sample = min(len(v), MAX_FRAMES_PER_ROOM)
        sampled_frames = sample(v, num_frames_to_sample)
        uploaded_frames[k] = sampled_frames
        total_sampled_frames += 1

    if verbose:
        for k, v in uploaded_frames.items():
            print(f"Uploading {len(v)} frames from room {k}")

        print(f"total_sampled_frames: {total_sampled_frames}")

    if write_tojson:
        write_frames_grouped_by_room_map_to_json(UPLOADED_FRAMES_FILENAME)

    return uploaded_frames


def write_frames_grouped_by_room_map_to_json(frames_by_rooms_map, filename):
    all_frames_json = json.dumps(frames_by_rooms_map, indent=9)
    with open(f"{JSON_WRITE_PATH}/{filename}", "w") as f:
        f.write(all_frames_json)


def get_frames_grouped_by_room_map(
    write_frames_rooms_maps_to_json=False, verbose=False
):
    frames_by_rooms_map = defaultdict(list)
    total_frames = 0
    for f in os.listdir(PATH_TO_FRAMES):
        if ".jpeg" in f:
            room = f.split("_")[0]
            frames_by_rooms_map[room].append(f"{PATH_TO_FRAMES}/{f}")
            total_frames += 1

    if verbose:
        for k, v in frames_by_rooms_map.items():
            print(f"Room {k} has {len(v)} rooms")

        print(f"total_frames: {total_frames}")

    if write_frames_rooms_maps_to_json:
        write_frames_grouped_by_room_map_to_json(
            frames_by_rooms_map, FRAMES_UNIVERSE_FILENAME
        )

    return frames_by_rooms_map


def exec_curl_cmd_to_upload_frame(abs_path_to_img_frame):
    curl_upload_cmd = f"curl -H 'Authorization: Token {constants.LABEL_STUDIO_ACCESS_TOKEN}' -X POST '{constants.LABEL_STUDIO_HOST}projects/{LABEL_STUDIO_PROJECT_ID}/import' -F 'file=@{abs_path_to_img_frame}'"

    exit_code = os.system(curl_upload_cmd)
    if exit_code != 0:
        print(
            f"Returned error code {exit_code} after trying to upload img frame {abs_path_to_img_frame}"
        )


def run(verbose=False):
    frames_by_rooms_map = get_frames_grouped_by_room_map()
    sampled_frames_to_upload = sample_frames_to_upload(frames_by_rooms_map)

    start_time = datetime.datetime.now()

    num_files_uploaded = 0
    for k, sampled_frames in sampled_frames_to_upload.items():
        for sampled_frame in sampled_frames:
            num_files_uploaded += 1
            exec_curl_cmd_to_upload_frame(sampled_frame)

    end_time = datetime.datetime.now()

    if verbose:
        upload_time = (end_time - start_time).total_seconds()
        print(f"It took {upload_time} seconds to upload {num_files_uploaded} img files")


if __name__ == "__main__":
    run(verbose=True)
