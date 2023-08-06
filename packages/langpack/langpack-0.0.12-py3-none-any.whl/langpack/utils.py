import ast
import importlib
import inspect
import json
import os
import pkgutil
import shutil
import subprocess
import sys
import zipfile
from types import FunctionType
from typing import Any, Dict, List, Tuple, Type, Union

import astor
import boto3
from dotenv import dotenv_values, load_dotenv


def delete_and_create_dir(dir_path: str) -> None:
    """
    Deletes and creates a directory.
    Args:
        dir_path (str): Path to the directory to be deleted and created.
    """
    if os.path.exists(dir_path):
        # If it does, delete it and recreate it
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    else:
        # If it doesn't, create it
        os.makedirs(dir_path)


def print_success(app_path: str) -> int:
    """
    Prints a success message.
    Args:
        app_path (str): Path to the app.
    Returns:
        int: 0, indicating success.
    """
    print(
        """
                  .--.           .---.        .-.
       .---|--|   .-.     | L |  .---. |~|    .--.
    .--|===|  |---|_|--.__| A |--|:::| |~|-==-|==|---.
    |%%|   |  |===| |~~|%%| M |--|   |_|~|    |  |___|-.
    |  |   |  |===| |==|  | B |  |:::|=| |    |  |---|=|
    |  |   |  |   |_|__|  | D |__|   | | |    |  |___| |
    |~~|===|--|===|~|~~|%%| A |--|:::|=|~|----|==|---|=|
    ^--^---'--^---^-^--^--^---'--^---^-^-^-==-^--^---^-"""
    )
    print(f"You app has been saved to {app_path}")
    print("--------------------------------------")
    print(
        "For apps generated using scripts from the examples folder, you can run the"
        " following command to test it: "
    )
    print(
        f"cd {app_path} && python -c 'from langpack.tester import test_package;"
        " test_package()' && cd - >/dev/null"
    )
    print("--------------------------------------")
    print("You can launch the app on your local machine with the following command: ")
    print(f"localtest {app_path}")
    print("--------------------------------------")
    print("Pack succeeded")
    return 0


def replace_word_in_file(file_path: str, old_word: str, new_word: str) -> int:
    """
    This function replaces all instances of a given word in a file with another word
    Arguments:
        file_path: The path to the file to replace words in
        old_word: The word to replace
        new_word: The new word to replace the old word with
    Returns:
        0 on success, or a nonzero error code on failure
    """
    # Read the file text
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_text = file.read()
    except FileNotFoundError:
        print(f"Could not find file {file_path}")
        return 1

    # Replace the old word with the new word in the file text
    new_file_text = file_text.replace(old_word, new_word)

    # Write the new file text
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_file_text)
    except FileNotFoundError:
        print(f"Could not write to file {file_path}")
        return 1

    # Return success
    return 0


def list_classes(module_name: str) -> List[Type[Any]]:
    """
    Lists all the classes in a module.
    Args:
        module_name (str): Name of the module.
    Returns:
        List[Type[Any]]: List of classes in the module.
    """
    classes = []
    # Try to import the module.
    try:
        module = importlib.import_module(module_name)
        # Iterate through all the members of the module.
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # If the member is a class, add it to the list.
            if obj.__module__ == module_name:
                classes.append(obj)

        # Iterate through all the submodules of the module.
        for _, name, is_pkg in pkgutil.walk_packages(module.__path__):
            # Get the full name of the submodule.
            full_name = module_name + "." + name
            # If the submodule is a package, recursively get the classes in the package.
            if is_pkg:
                classes += list_classes(full_name)
            # If the submodule is not a package, try to import it and get its classes.
            else:
                try:
                    sub_module = importlib.import_module(full_name)
                    for name, obj in inspect.getmembers(sub_module, inspect.isclass):
                        if obj.__module__ == full_name:
                            classes.append(obj)
                # If the submodule can not be imported, skip it.
                except ImportError:
                    print(f"module {full_name} can not be loaded.")
    # If the module can not be imported, skip it.
    except ImportError:
        print(f"module {module_name} can not be loaded.")
    return classes


def list_classes_from_file(module_name: str) -> List[Type]:
    """
    Lists all the classes in a module when the module is a python file.
    Args:
        module_name (str): Name of the module (python file).
    Returns:
        List[Type[Any]]: List of classes in the module.
    """
    # Import the module by name
    module = importlib.import_module(module_name)

    # Get the filename of the module
    filename = inspect.getfile(module)

    # Get a list of classes from the module
    classes = [
        obj
        for _, obj in inspect.getmembers(module, inspect.isclass)
        # Filter classes to only include those from the file
        if inspect.getfile(obj) == filename
    ]
    return classes


def list_functions_from_file(module_name: str) -> List[str]:
    """
    Lists all the functions in a module when the module is a python file.
    Args:
        module_name (str): Name of the module (python file).
    Returns:
        List[str]: List of functions in the module.
    """
    # Load the module
    spec = importlib.util.spec_from_file_location("module.name", module_name + ".py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get all the functions defined in the module
    functions = inspect.getmembers(module, inspect.isfunction)

    # Filter out imported modules and the main function
    functions = [
        function[0]
        for function in functions
        if function[0] not in ("main", "__builtins__")
        and function[1].__module__ == module.__name__
    ]

    return functions


def is_list_of_strings(obj: object) -> bool:
    """
    Checks if an object is a list of strings.
    Args:
        obj (object): The object to check.
    Returns:
        bool: True if the object is a list of strings, False otherwise.
    """
    # Check if obj is a list
    if not isinstance(obj, list):
        return False

    # Check if all items in the list are strings
    return all(isinstance(item, str) for item in obj)


def is_json_serializable(obj: object) -> bool:
    """
    Checks if an object is JSON serializable.
    Args:
        obj (object): The object to check.
        Returns:
        bool: True if the object is JSON serializable, False otherwise.
    """
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False


def find_obj_dynamic(
    script_path: str, class_list: List[str]
) -> Tuple[str, str, object]:
    """
    Finds the last object of interests in a script.
    Args:
        script_path (str): Path to the script.
        class_list (List[str]): List of classes of interests to search for.
    Returns:
        Tuple[str, str, object]: The name of the class, the name of the object, and the object.
    """

    # Add the script's directory to the system path
    script_dir = os.path.dirname(script_path)
    sys.path.append(script_dir)

    # Read the script file
    with open(script_path, "r", encoding="utf-8") as file:
        script = file.read()

    # change working dir to the script's directory in cas there are reference path for other code/data
    os.chdir(os.path.join(os.getcwd(), "/".join(script_path.split("/")[:-1])))
    current_directory = os.getcwd()
    print(current_directory)

    # Create a custom namespace for executing the script
    namespace: Dict[str, object] = {}

    # Execute the script in the custom namespace
    # XXX: THIS IS DANGEROUS, must run in a docker container
    # TODO: Find a safer way to execute the script
    exec(script, namespace)

    # Remove the script's directory from the system path
    sys.path.remove(script_dir)

    # Iterate over the namespace items and filter objects based on class names
    matching_objects = [
        (name, obj.__class__.__name__, obj)
        for name, obj in namespace.items()
        if obj.__class__.__name__ in class_list and not isinstance(obj, FunctionType)
    ]

    # Return the last matching object or None if no matches are found
    return matching_objects[-1] if matching_objects else (None, None, None)


def build_lib(path: str) -> str:
    """
    Builds a library file from a script.
    The library file should only contain the imports, custom function and class definitions.
    Args:
        path (str): Path to the script.
    Returns:
        str: Path to the library file.
    """
    # Parse the source code of the script
    with open(path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())

    # Extract the necessary imports, custom function and class definitions
    imports: List[ast.stmt] = []
    defs: List[Union[ast.FunctionDef, ast.ClassDef]] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.append(node)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node)
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            defs.append(node)

    # Generate the code for the library file
    code = ast.Module(body=imports + defs)
    lib_path = "lib_" + os.path.basename(path)
    with open(lib_path, "w", encoding="utf-8") as file:
        file.write(astor.to_source(code))
    return lib_path


def launch_api_local(shell_commands: List[str]) -> int:
    """
    Launches the API locally.
    Args:
        shell_commands (List[str]): List of shell commands to run.
    Returns:
        0 on success, or a nonzero error code on failure
    """
    if not shell_commands:
        print("No shell commands provided")
        return

    # Check if tmux session already exists
    session_exists = False
    try:
        subprocess.run(["tmux", "has-session", "-t", "api_session"], check=True)
        session_exists = True
    except subprocess.CalledProcessError:
        pass

    # Create a new tmux session if it doesn't already exist
    if not session_exists:
        subprocess.run(
            ["tmux", "new-session", "-s", "api_session", "-d"],
            check=True,
        )

    # Run the commands in the first window
    try:
        subprocess.run(
            [
                "tmux",
                "send-keys",
                "-t",
                "api_session:window0",
                f"{shell_commands[0]}",
                "Enter",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"Error: {error}")

    # Create horizontal panes and run a command in them for the rest of the commands
    for command in shell_commands[0:]:
        try:
            subprocess.run(
                ["tmux", "split-window", "-t", "api_session", "-h"], check=True
            )
        except subprocess.CalledProcessError as error:
            print(f"Error: {error}")

        try:
            subprocess.run(
                ["tmux", "send-keys", "-t", "api_session", f"{command}", "Enter"],
                check=True,
            )
        except subprocess.CalledProcessError as error:
            print(f"Error: {error}")

    # Adjust the layout of the panes to 'even-horizontal'
    try:
        subprocess.run(
            ["tmux", "select-layout", "-t", "api_session", "even-horizontal"],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"Error: {error}")

    # Attach to the tmux session
    try:
        subprocess.run(["tmux", "attach-session", "-t", "api_session"], check=True)
    except subprocess.CalledProcessError as error:
        print(f"Error: {error}")
    else:
        return 0


def parse_env_dict(env_dict: dict) -> str:
    """
    Parses a dictionary of environment variables into a string.
    Args:
        env_dict (dict): Dictionary of environment variables.
    Returns:
        str: String of environment variables.
    """
    env_vars = []
    for key, value in env_dict.items():
        env_vars.append(f'-e {key}="{value}"')

    return " ".join(env_vars)


def run_command(command: str) -> int:
    """
    Runs a command in the shell.
    Args:
        command (str): Command to run.
    Returns:
        0 on success, or a nonzero error code on failure
    """
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"Error: {error}")

    if result.returncode == 0:
        print(f"{command} completed successfully.")
        print(result.stdout.strip())
        return 0
    else:
        print(result.stderr.strip())
        raise f"{command} failed."


def run_ssh_command(hostname: str, username: str, ssh_key: str, command: str) -> int:
    """
    Runs a command on a remote server via SSH.
    Args:
        hostname (str): Hostname of the remote server.
        username (str): Username to use for SSH.
        ssh_key (str): Path to the SSH key.
        command (str): Command to run.
    Returns:
        0 on success, or a nonzero error code on failure
    """
    ssh_command = f"ssh -i {ssh_key} {username}@{hostname} {command}"

    try:
        subprocess.run(
            ssh_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return 0
    except subprocess.CalledProcessError as error:
        print(f"Error: {error}")


def zip_and_upload_to_s3(
    source_folder: str, destination_bucket: str, destination_key: str, region: str
) -> int:
    """
    Zips a folder and uploads it to S3.
    Args:
        source_folder (str): Local path to the folder to zip.
        destination_bucket (str): Name of the S3 bucket to upload to.
        destination_key (str): Name of the S3 key to upload to.
        region (str): Name of the AWS region.
    Returns:
        0 on success, or a nonzero error code on failure
    """
    # Create a new zip file
    zip_filename = source_folder + ".zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add all files in the source folder to the zip file
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, file_path.replace(source_folder, "", 1))

    # Upload the zip file to S3
    s3_client = boto3.client("s3", region_name=region)
    with open(zip_filename, "rb") as data:
        s3_client.upload_fileobj(data, destination_bucket, destination_key)

    # Clean up the temporary zip file
    os.remove(zip_filename)

    return 0


def download_and_unzip_file_from_s3(
    target_file_path: str, bucket_name: str, file_key: str, region: str
) -> str:
    """
    Downloads a file from S3 and unzips it.
    Args:
        target_file_path (str): Local path to download the zip file to.
        bucket_name (str): Name of the S3 bucket to download from.
        file_key (str): Name of the S3 key to download.
        region (str): Name of the AWS region.
    Returns:
        str: Local path to the unzipped file.
    """
    s3_client = boto3.client("s3", region_name=region)
    try:
        s3_client.download_file(bucket_name, file_key, target_file_path)
        print(f"File downloaded successfully to {target_file_path}")

        # Unzip the downloaded file
        unzip_path = ".".join(target_file_path.split(".")[:-1])
        with zipfile.ZipFile(target_file_path, "r") as zip_ref:
            zip_ref.extractall(unzip_path)
        print(f"File unzipped successfully to {unzip_path}")

        return unzip_path

    except Exception as error:
        print(f"Error downloading or unzipping file: {error}")


def config_deployment_lambda() -> dict:
    """
    Configures the deployment on Lambda instance.
    Returns:
        dict: Dictionary of deployment configuration.
    """
    deployment_config = {}
    deployment_config["ssh_key"] = os.environ["LAMBDA_SSH_KEY"]
    deployment_config["remote_ip"] = os.environ["LAMBDA_IP"]
    deployment_config["username"] = os.environ["LAMBDA_USER_NAME"]
    deployment_config["docker_image"] = os.environ["DOCKER_IMAGE"]
    deployment_config["default_app_path"] = os.environ["LAMBDA_DEFAULT_APP_PATH"]
    deployment_config["default_home_path"] = os.environ["LAMBDA_DEFAULT_HOME_PATH"]

    if not deployment_config["ssh_key"]:
        print("Please set the LAMBDA_SSH_KEY environment variable")
        sys.exit(1)
    if not deployment_config["remote_ip"]:
        print("Please set the LAMBDA_IP environment variable")
        sys.exit(1)
    if not deployment_config["username"]:
        print("Please set the LAMBDA_USER_NAME environment variable")
        sys.exit(1)
    if not deployment_config["docker_image"]:
        print("Please set the DOCKER_IMAGE environment variable")
        sys.exit(1)

    return deployment_config


def config_deployment_aws() -> dict:
    """
    Configures the deployment on AWS instance.
    Returns:
        dict: Dictionary of deployment configuration.
    """
    deployment_config = {}
    deployment_config["ssh_key"] = os.environ["AWS_SSH_KEY"]
    deployment_config["remote_ip"] = os.environ["AWS_IP"]
    deployment_config["username"] = os.environ["AWS_USER_NAME"]
    deployment_config["docker_image"] = os.environ["DOCKER_IMAGE"]
    deployment_config["default_app_path"] = os.environ["AWS_DEFAULT_APP_PATH"]
    deployment_config["default_home_path"] = os.environ["AWS_DEFAULT_HOME_PATH"]

    if not deployment_config["ssh_key"]:
        print("Please set the AWS_SSH_KEY environment variable")
        sys.exit(1)
    if not deployment_config["remote_ip"]:
        print("Please set the AWS_IP environment variable")
        sys.exit(1)
    if not deployment_config["username"]:
        print("Please set the AWS_USER_NAME environment variable")
        sys.exit(1)
    if not deployment_config["docker_image"]:
        print("Please set the DOCKER_IMAGE environment variable")
        sys.exit(1)

    return deployment_config


def create_dict_class(filename: str) -> dict:
    """
    Creates a dictionary of classes of interests from langchain library plus a custom script.
    Args:
        filename (str): Name of the custom script file.
    Returns:
        dict: Dictionary of classes of interests.
    """
    dict_class = {
        "list_class_llm": [c.__name__ for c in list_classes("langchain.llms")],
        "list_class_prompt": [c.__name__ for c in list_classes("langchain.prompts")],
        "list_class_utility": [c.__name__ for c in list_classes("langchain.utilities")],
        "list_class_chain": [c.__name__ for c in list_classes("langchain.chains")],
        "list_class_agent": [c.__name__ for c in list_classes("langchain.agents")],
        "list_class_vectorstore": [
            c.__name__ for c in list_classes("langchain.vectorstores")
        ],
        "list_class_embedding": [
            c.__name__ for c in list_classes("langchain.embeddings")
        ],
        "list_class_requestwrapper": [
            c.__name__ for c in list_classes_from_file("langchain.requests")
        ],
        "list_class_tool": [c.__name__ for c in list_classes("langchain.tools")],
        "list_class_memory": [c.__name__ for c in list_classes("langchain.memory")],
        "list_class_custom": [c.__name__ for c in list_classes_from_file(filename)],
        "list_class_chatmodel": [
            c.__name__ for c in list_classes("langchain.chat_models")
        ],
        "list_class_index": [c.__name__ for c in list_classes("langchain.indexes")],
        "list_class_docstore": [c.__name__ for c in list_classes("langchain.docstore")],
        "list_class_transformers_pipeline": [
            c.__name__ for c in list_classes("transformers.pipelines")
        ],
        "list_class_function": ["function"],
        "list_class_method": ["method"],
    }

    # dict_class["list_class_agent"].remove("Tool")
    dict_class["list_class_tool"].append("Tool")

    dict_class["list_class"] = (
        ["list"]
        + dict_class["list_class_llm"]
        + dict_class["list_class_prompt"]
        + dict_class["list_class_utility"]
        + dict_class["list_class_chain"]
        + dict_class["list_class_agent"]
        + dict_class["list_class_vectorstore"]
        + dict_class["list_class_embedding"]
        + dict_class["list_class_requestwrapper"]
        + dict_class["list_class_tool"]
        + dict_class["list_class_memory"]
        + dict_class["list_class_chatmodel"]
        + dict_class["list_class_index"]
        + dict_class["list_class_docstore"]
        + dict_class["list_class_function"]
        + dict_class["list_class_transformers_pipeline"]
        + dict_class["list_class_method"]
        + dict_class["list_class_custom"]
    )

    return dict_class


def get_type(type_name: str, dict_class: dict) -> str:
    """
    Gets the type of the class.
    Args:
        type_name (str): Name of the class.
        dict_class (dict): Dictionary of classes of interests.
    Returns:
        str: Type of the class.
    """
    type_name = type_name.split(".")[-1]
    if type_name in dict_class["list_class_chain"]:
        return "chain"
    elif type_name in dict_class["list_class_agent"]:
        return "agent"
    elif type_name in dict_class["list_class_vectorstore"]:
        return "vectorstore"
    elif type_name in dict_class["list_class_embedding"]:
        return "embedding"
    elif type_name in dict_class["list_class_requestwrapper"]:
        return "request_wrapper"
    elif type_name in dict_class["list_class_tool"]:
        return "tool"
    elif type_name in dict_class["list_class_memory"]:
        return "memory"
    elif type_name in dict_class["list_class_prompt"]:
        return "prompt"
    elif type_name in dict_class["list_class_llm"]:
        return "llm"
    elif type_name in dict_class["list_class_custom"]:
        return "custom"
    elif type_name in dict_class["list_class_chatmodel"]:
        return "chatmodel"
    elif type_name in dict_class["list_class_index"]:
        return "index"
    elif type_name in dict_class["list_class_docstore"]:
        return "docstore"
    elif type_name in dict_class["list_class_function"]:
        return "function"
    elif type_name in dict_class["list_class_method"]:
        return "method"
    elif type_name in dict_class["list_class_transformers_pipeline"]:
        return "transformers_pipeline"
    elif type_name in dict_class["list_class_utility"]:
        return "utility"
    elif type_name == "list":
        return "list"
    else:
        raise Exception(f"langpack doesn't support type {type_name}")


def load_env(env_path: str) -> dict:
    """
    Loads the environment variables from the .env file.
    Args:
        env_path (str): Path to the .env file.
    Returns:
        env_str (str): String of environment variables in the format of -e KEY=\"VALUE\".
    """

    # Check if the env file exists
    if os.path.exists(env_path):
        # Load the .env file and parse it into a dictionary
        load_dotenv(env_path)
        env_dict = dotenv_values(env_path)
        # Convert the dictionary into a string
        env_str = parse_env_dict(env_dict)
    else:
        print(
            "WARNING: No .env file found in ~/.langpack/.env, it is recommended to create one."
        )
        env_str = ""

    return env_str
