import argparse
import json
import os
import shutil
import sys
from typing import Any

from langpack.tools import _deserialize, _package, _serialize
from langpack.utils import (
    build_lib,
    config_deployment_aws,
    config_deployment_lambda,
    create_dict_class,
    download_and_unzip_file_from_s3,
    find_obj_dynamic,
    launch_api_local,
    load_env,
    run_command,
    run_ssh_command,
    zip_and_upload_to_s3,
)

# Environment variables are expected to be defined in ~/.langpack/.env
ENV_VAR_PATH = os.path.join(os.path.expanduser("~"), ".langpack/.env")


def pack(script_path: str = "", port: int = 7002) -> str:
    """
    Takes a Python langchain script file path as the input and pack the app.
    args:
        script_path: Python script file path
    reutrn:
        output_path: Path to the packed app
    """
    if not script_path:
        parser = argparse.ArgumentParser()
        parser.add_argument("script_path", help="Langchain Python script file path")
        args = parser.parse_args()

        # Setup the path
        script_path = args.script_path
        
    module_path, _ = os.path.splitext(script_path)

    # Load the env variables
    _ = load_env(ENV_VAR_PATH)

    # use script_path as the working directory
    os.chdir(os.path.join(os.getcwd(), "/".join(module_path.split("/")[:-1])))
    current_directory = os.getcwd()

    # update sys.path so the script can be imported (needed for gethering custom classes implemented in that file)
    sys.path.insert(0, current_directory)

    script_path = os.path.basename(script_path)
    module_path, _ = os.path.splitext(script_path)

    app_name = module_path.split(".")[-1]
    os.environ["SOURCE_NAME"] = app_name
    print(f"script_path: {script_path}")
    print(f"app_name: {app_name}")
    print(f"current_directory: {current_directory}")
    print("Import search paths: ------------------")
    for path in sys.path:
        print(path)

    # Build lib_script.py, which only contains imports and custom classes and functions
    lib_script_path = build_lib(script_path)
    lib_module_path, _ = os.path.splitext(lib_script_path)
    print(f"lib_module_path: {lib_module_path}")
    print("---------------------------------------")

    # build a dict_class (dictionary of langchain classes and custom classes)
    dict_class = create_dict_class(lib_module_path)
    print("list_class: ")
    print(dict_class["list_class"])
    print("list_class_custom: ")
    print(dict_class["list_class_custom"])
    print("---------------------------------------")

    # Run the script and get the app object
    obj_name, obj_type, obj = find_obj_dynamic(script_path, dict_class["list_class"])

    print("App Object: ")
    print(f"obj_name: {obj_name}")
    print(f"obj_type: {obj_type}")
    print(obj)
    print("---------------------------------------")

    if not obj_name:
        raise ValueError("No object of interests can be found.")

    # pack: serialize the objects
    dependency_dict = _serialize(obj, dict_class)

    print("---------------------------------------")
    print("dependency_dict: ")
    print(json.dumps(dependency_dict, indent=4))
    print("---------------------------------------")

    app = {}
    app["source_name"] = app_name
    app["dependency_dict"] = dependency_dict

    # pack: create package
    output_path = _package(app, app_name, script_path, lib_module_path)

    return output_path


def unpack(app_config_path) -> Any:
    """Takes a packed app and reinstantiate the app object
    args:
        app_config_path: Path to the packed app
    return:
        app: App object
    """

    # Load the env variables
    _ = load_env(ENV_VAR_PATH)

    current_directory = os.getcwd()
    # update sys.path so the script can be imported
    # (needed for gethering custom classes implemented in that file)
    sys.path.insert(0, current_directory)

    print(f"current_directory: {current_directory}")
    print("Import search paths: ------------------")
    for path in sys.path:
        print(path)
    print("---------------------------------------")

    with open(app_config_path, "r", encoding="utf-8") as file:
        # Load the JSON data into a Python dictionary
        app_config = json.load(file)
        print(app_config)

    dict_class = create_dict_class("lib_" + app_config["source_name"])
    app = _deserialize(app_config["dependency_dict"], dict_class)
    return app


def localtest():
    """
    Takes a package path and launch a flask backend service and a client to post request
    A flask backend service is launched at http://127.0.0.1:5000/predict
    A client launched in a terminal window to post request to the backend service
    args:
        app_path: Path to the packed app
    Returns:
        0 on success, or a nonzero error code on failure
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("app_path", help="Python script file path")
    args = parser.parse_args()

    # Load the env variables
    _ = load_env(ENV_VAR_PATH)

    # Launch the flask backend service and the client
    commands = [
        f"cd {args.app_path} && source $VIRTUAL_ENV/bin/activate && python app.py",
        f"cd {args.app_path} && source $VIRTUAL_ENV/bin/activate && python client.py",
    ]

    _ = launch_api_local(commands)


def push() -> int:
    """
    Push the packed app to the cloud instance
    args:
        app_path: Path to the packed app
        instance: Type of instance (lambda, aws)
    Returns:
        0 on success, or a nonzero error code on failure
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("app_path", help="Local path of the app")
    parser.add_argument(
        "--instance",
        type=str,
        choices=["lambda", "aws"],
        default="lambda",
        help="Type of instance",
    )
    args = parser.parse_args()

    # Load the env variables
    _ = load_env(ENV_VAR_PATH)

    if args.instance == "lambda":
        lambda_cloud_key = os.environ["LAMBDA_SSH_KEY"]
        remote_ip = os.environ["LAMBDA_IP"]
        if not lambda_cloud_key:
            print("Please set the LAMBDA_SSH_KEY environment variable")
            sys.exit(1)
        if not remote_ip:
            print("Please set the REMOTE_IP environment variable")
            sys.exit(1)

        # scp the app to Lambda cloud instance
        command = f"scp -r -i {lambda_cloud_key} {args.app_path} {remote_ip}:~/"
        success_flag = run_command(command)
        return success_flag
    elif args.instance == "aws":
        destination_key = (
            os.environ["AWS_S3_BUCKET_APP_PATH"]
            + "/"
            + args.app_path.split("/")[-1]
            + ".zip"
        )
        # zip and upload to S3
        success_flag = zip_and_upload_to_s3(
            args.app_path,
            os.environ["AWS_S3_BUCKET"],
            destination_key,
            os.environ["AWS_S3_REGION"],
        )
        return success_flag
    else:
        raise f"Instance type {args.instance} is not supported"


def deploy() -> int:
    """
    Deploy the app to the cloud instance
    args:
        app_url: Path to the packed app on s3 bucket
        app_path: Path to the packed app on the cloud instance
        instance: Type of instance (lambda, aws)
        environ_file: Path to env.list file that stores the environment variables like API keys
    Returns:
        0 on success, or a nonzero error code on failure
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--instance",
        type=str,
        choices=["lambda", "aws"],
        default="lambda",
        help="Type of instance",
    )
    parser.add_argument("--app_url", default="", help="URL for fetching the app")
    parser.add_argument("--app_path", default="", help="Path of app on the instance")
    parser.add_argument(
        "--environ_file",
        type=str,
        default="",
        help=(
            "Path to env.list file that stores the environment variables like API keys"
        ),
    )
    args = parser.parse_args()

    # Load the env variables
    env_str = load_env(ENV_VAR_PATH)

    # one of app_path and app_url needs to be set
    if not args.app_path and not args.app_url:
        print(
            "Error: app_path and app_url are both missing. One of them needs to be set"
        )
        sys.exit(1)

    # Load the deployment config for the type of instance
    if args.instance == "lambda":
        deployment_config = config_deployment_lambda()
    elif args.instance == "aws":
        deployment_config = config_deployment_aws()
    else:
        raise f"Instance type {args.instance} is not supported"

    ssh_key = deployment_config["ssh_key"]
    remote_ip = deployment_config["remote_ip"]
    username = deployment_config["username"]
    docker_image = deployment_config["docker_image"]
    default_app_path = deployment_config["default_app_path"]
    default_home_path = deployment_config["default_home_path"]

    if args.app_url:
        # for app_url, download app to that app folder
        # (currently only supports s3 bucket)
        fetch_app_command = (
            "sudo docker run --pull always --network host -v"
            f" {default_home_path}:/workspace"
            f" {env_str} {docker_image} download_app_from_s3 {args.app_url}"
        )
        print("fetch the app from url:")
        print(fetch_app_command)
        print("-----------------------------------------------")
        _ = run_ssh_command(remote_ip, username, ssh_key, fetch_app_command)
    else:
        # otherwise assuming the app is already downloaded on the instance, just need to cp it to the default app path
        print("fetch the app from a local copy:")
        print("try removing existing app:")
        fetch_app_command = f"sudo rm -r {default_app_path}"
        print(fetch_app_command)
        _ = run_ssh_command(remote_ip, username, ssh_key, fetch_app_command)
        print("-----------------------------------------------")
        print("try copy app to the correct location:")
        fetch_app_command = f"sudo cp -r {args.app_path} {default_app_path}"
        print(fetch_app_command)
        _ = run_ssh_command(remote_ip, username, ssh_key, fetch_app_command)
        print("-----------------------------------------------")

    # Launch the app using docker
    launch_app_command = (
        f"nohup sudo docker run --pull always --network host -v {default_app_path}:/app"
        f" {env_str} -w /app {docker_image} python3 app.py > /dev/null 2>&1 &"
    )

    print("launch_app_command: ")
    print(launch_app_command)
    print("-----------------------------------------------")
    success_flag = run_ssh_command(remote_ip, username, ssh_key, launch_app_command)

    print(f"App launched at http://{remote_ip}:5000/predict")

    return success_flag


def download_app_from_s3() -> int:
    """
    Download the app from S3 and unzip it
    args:
        s3_url: S3 bucket URL for fetching the app
    returns:
        0 on success, or a nonzero error code on failure
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("s3_url", default="", help="S3 bucket URL for fetching the app")
    args = parser.parse_args()

    # download and unzip
    cache_path = "/"
    bucket_name = os.environ["AWS_S3_BUCKET"]
    region = os.environ["AWS_S3_REGION"]
    file_key = args.s3_url
    target_file_path = os.path.join(cache_path, file_key.split("/")[-1])
    print(target_file_path)
    unzip_path = download_and_unzip_file_from_s3(
        target_file_path, bucket_name, file_key, region
    )

    app_path = "/workspace/app"

    # Check if the target path already exists
    if os.path.exists(app_path):
        # Remove the existing directory
        shutil.rmtree(app_path)

    # Move the unzipped directory to the target path
    shutil.move(unzip_path, app_path)

    print(f"App successfully unzipped to {app_path}")

    return 0
