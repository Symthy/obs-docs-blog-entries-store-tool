import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List


def exist_file(target_dir_path: str) -> any:
    return os.path.exists(target_dir_path) and os.path.isfile(target_dir_path)


def exist_dir(target_dir_path: str) -> bool:
    return os.path.exists(target_dir_path) and os.path.isdir(target_dir_path)


def join_path(*paths: str):
    return os.path.join(*paths)


def get_dir_names_in_target_dir(target_dir_path: str) -> List[str]:
    files = os.listdir(target_dir_path)
    return [d for d in files if os.path.isdir(join_path(target_dir_path, d))]


def get_file_paths_in_target_dir(target_dir_path: str) -> List[str]:
    files = os.listdir(target_dir_path)
    return [target_dir_path + f for f in files if os.path.isfile(os.path.join(target_dir_path, f))]


def get_dir_name_from_dir_path(path: str) -> str:
    if path.endswith('/'):
        # dir path: xxx/
        return path[:-1].rsplit('/', 1)[1]
    return path.rsplit('/', 1)[1]


def get_file_name_from_file_path(path: str) -> str:
    return path.rsplit('/', 1)[1]


def get_dir_path_from_file_path(path: str) -> str:
    return path.rsplit('/', 1)[0]


def get_file_paths_in_target_dir(target_dir_path: str) -> List[str]:
    files = os.listdir(target_dir_path)
    return [target_dir_path + f for f in files if os.path.isfile(os.path.join(target_dir_path, f))]


def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path)


def get_file_name_without_ext(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]


def get_created_file_time(file_path: str) -> datetime:
    created_unix_time = Path(file_path).stat().st_ctime
    created_date_time = datetime.fromtimestamp(created_unix_time)
    return created_date_time


def get_updated_file_time(file_path: str) -> datetime:
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def copy_file(from_path: str, to_path: str):
    shutil.copy2(from_path, to_path)


def remove_file(file_path: str):
    os.remove(file_path)
