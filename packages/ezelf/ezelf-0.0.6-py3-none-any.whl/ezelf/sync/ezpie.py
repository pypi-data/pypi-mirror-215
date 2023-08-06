import os
import shutil
import tarfile
import tempfile
import zipfile
from typing import List

WORKING_DIR = "/home/workspace"
ARTIFACTS_DIR = "/home/artifacts"

TAR_ARCHIVE_NAME = "archive.tar.gz"
ZIP_ARCHIVE_NAME = "archive.zip"


def ezecho(input):
    return input


def copy_dir(dir: str = None, dest_dir: str = None, include_hidden_files=False):
    """将目录下的文件打包并拷贝到 artifacts 目录"""
    if dir is None:
        dir = WORKING_DIR
    if dest_dir is None:
        dest_dir = ARTIFACTS_DIR

    create_zip_archive_from_dir(dir, dest_dir, ZIP_ARCHIVE_NAME)


def copy_files(file_list: List[str], dest_dir: str):
    """将文件打包并拷贝到 artifacts 目录"""
    if dest_dir is None:
        dest_dir = ARTIFACTS_DIR

    create_zip_archive_from_file_list(file_list, dest_dir, ZIP_ARCHIVE_NAME)


# **************** utils ****************


def create_zip_archive_from_dir(source_dir, destination_dir, archive_name):
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 创建 zip 文件
    archive_path = os.path.join(temp_dir, archive_name)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 遍历源目录中的所有文件和子目录
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, source_dir))

    # 将生成的 zip 文件移动到目标目录
    destination_path = os.path.join(destination_dir, archive_name)
    shutil.move(archive_path, destination_path)

    # 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 返回 zip 文件的路径
    return destination_path


def create_tar_archive_from_dir(source_dir, destination_dir, archive_name):
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 创建 tar.gz 文件
    archive_path = os.path.join(temp_dir, archive_name)
    with tarfile.open(archive_path, "w:gz") as tar:
        # 遍历源目录中的所有文件和子目录
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.relpath(file_path, source_dir))

    # 将生成的 tar 包移动到目标目录
    destination_path = os.path.join(destination_dir, archive_name)
    shutil.move(archive_path, destination_path)

    # 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 返回 tar.gz 文件的路径
    return destination_path


def create_zip_archive_from_file_list(files, destination_dir, archive_name):
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 找到路径最浅的文件
    base_dir = os.path.commonpath(files)

    # 创建 zip 文件
    archive_path = os.path.join(temp_dir, archive_name)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件列表
        for file_path in files:
            if os.path.isfile(file_path):  # 确保文件存在
                # 计算相对路径
                rel_path = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname=rel_path)

    # 将生成的 zip 文件移动到目标目录
    destination_path = os.path.join(destination_dir, archive_name)
    shutil.move(archive_path, destination_path)

    # 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 返回 zip 文件的路径
    return destination_path


def create_tar_archive_from_file_list(files, destination_dir, archive_name):
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 找到路径最浅的文件
    base_dir = os.path.commonpath(files)

    # 创建 tar 文件
    archive_path = os.path.join(temp_dir, archive_name)
    with tarfile.open(archive_path, "w:gz") as tar:
        # 遍历文件列表
        for file_path in files:
            if os.path.isfile(file_path):  # 确保文件存在
                # 计算相对路径
                rel_path = os.path.relpath(file_path, base_dir)
                tar.add(file_path, arcname=rel_path)

    # 将生成的 tar 文件移动到目标目录
    destination_path = os.path.join(destination_dir, archive_name)
    shutil.move(archive_path, destination_path)

    # 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 返回 tar 文件的路径
    return destination_path
