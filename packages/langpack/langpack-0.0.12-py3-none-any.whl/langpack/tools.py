import importlib
import inspect
import json
import os
import shutil
import time
from typing import Any, Dict, Type

from langchain import HuggingFacePipeline

from langpack.utils import (
    delete_and_create_dir,
    get_type,
    is_json_serializable,
    is_list_of_strings,
    print_success,
    replace_word_in_file,
)

LIST_API_KEYS = ["serpapi_api_key", "openai_api_key"]


def pack_function(obj: Any, dict_class: Dict[str, Any]) -> Dict[str, Any]:
    """Pack a function into the dictionary of dependancies.
    Args:
        obj: Python object to be packed.
    Returns:
        dict: updated dictionary of classes of interests.
    """

    # Need to find the module name or the script name (if the function is defined in a script)
    if not obj.__module__:
        obj.__module__ = os.environ["SOURCE_NAME"]
    obj_dict = {
        "type": "function",
        "deps": {},
        "kwargs": {"path": obj.__module__ + "." + obj.__name__},
    }

    return obj_dict


def pack_method(obj: Any, dict_class: Dict[str, Any]) -> Dict[str, Any]:
    """Pack a class method into the dictionary of dependancies.
    Args:
        obj: Python object to be packed.
    Returns:
        dict: updated dictionary of classes of interests.
    """

    # Need to serialize the class object first
    obj_dict = {
        "type": "method",
        "deps": {"__self__": _serialize(obj.__self__, dict_class)},
        "kwargs": {"__func__.__name__": obj.__func__.__name__},
    }
    return obj_dict


def pack_general(obj: Any, dict_class: Dict[str, Any]) -> Dict[str, Any]:
    """Pack a general Python object into the dictionary of dependancies.
    Args:
        obj: Python object to be packed.
    Returns:
        dict: updated dictionary of classes of interests.
    """

    # For general Python object we simply serialize it
    if hasattr(obj, "__dict__"):
        return _serialize(obj, dict_class)
    else:
        return None


def unpack_embedding(
    dict: Dict[str, Any], upacked_dict: Dict[str, Any], dict_class: Dict[str, Any]
) -> Any:
    """Unpack an embedding object from a dictionary.
    Args:
        dict: dictionary of the embedding object.
        upacked_dict: the unpacked attributes of the embedding object.
        dict_class: dictionary of classes of interests.
    Returns:
        obj: the unpacked embedding object.
    """
    module_name = ".".join(dict["type"].split(".")[:-1])
    class_name = dict["type"].split(".")[-1]
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)

    # delete redundant keys (so far only embedding object has redundant keys)
    if "model" in upacked_dict:
        if "document_model_name" in upacked_dict:
            del upacked_dict["document_model_name"]
        if "query_model_name" in upacked_dict:
            del upacked_dict["query_model_name"]

    argspec = inspect.getfullargspec(class_obj.__init__).args[1:]
    if argspec:
        upacked_dict = {k: v for k, v in upacked_dict.items() if k in argspec}

    obj = class_obj(**upacked_dict)
    return obj


def unpack_vectorstore(
    dict: Dict[str, Any], upacked_dict: Dict[str, Any], dict_class: Dict[str, Any]
) -> Any:
    """Unpack an vector store object from a dictionary.
    Args:
        dict: dictionary of the vector store object.
        upacked_dict: the unpacked attributes of the vector store object.
        dict_class: dictionary of classes of interests.
    Returns:
        obj: the unpacked vector store object.
    """
    module_name = ".".join(dict["type"].split(".")[:-1])
    class_name = dict["type"].split(".")[-1]
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)

    # Load from persistent storage
    obj = None
    if "retriever" in str(class_obj).lower():
        argspec = inspect.getfullargspec(class_obj.__init__).args[1:]
        if argspec:
            upacked_dict = {k: v for k, v in upacked_dict.items() if k in argspec}
        obj = class_obj(**upacked_dict)
    else:
        if "chroma" in str(class_obj).lower():
            obj = class_obj(
                persist_directory=upacked_dict["_persist_directory"],
                embedding_function=upacked_dict["_embedding_function"]
                if "_embedding_function" in upacked_dict
                else None,
            )
        elif "faiss" in str(class_obj).lower():
            obj = class_obj.load_local(
                folder_path=os.environ["VECTORSTORE_DIR"],
                embeddings=upacked_dict["embedding_function"].__self__,
            )
    return obj


def unpack_function(
    dict: Dict[str, Any], upacked_dict: Dict[str, Any], dict_class: Dict[str, Any]
) -> Any:
    """Unpack an function object from a dictionary.
    Args:
        dict: dictionary of the function object.
        upacked_dict: the unpacked attributes of the function object.
        dict_class: dictionary of classes of interests.
    Returns:
        obj: the unpacked function object.
    """
    function_path = dict["kwargs"]["path"]
    module_path = ".".join(function_path.split(".")[:-1])
    func_name = function_path.split(".")[-1]
    module = importlib.import_module(module_path)
    obj = getattr(module, func_name)
    return obj


def unpack_method(
    dict: Dict[str, Any], upacked_dict: Dict[str, Any], dict_class: Dict[str, Any]
) -> Any:
    """Unpack an member method object from a dictionary.
    Args:
        dict: dictionary of the member method object.
        upacked_dict: the unpacked attributes of the member method object.
        dict_class: dictionary of classes of interests.
    Returns:
        obj: the unpacked member method object.
    """
    # Need to deserialize the class object this member function belongs to first
    self_obj = _deserialize(dict["deps"]["__self__"], dict_class)
    return getattr(self_obj, dict["kwargs"]["__func__.__name__"])


def unpack_transformers_pipeline(
    dict: Dict[str, Any], upacked_dict: Dict[str, Any], dict_class: Dict[str, Any]
) -> Any:
    """Unpack a transformer pipeline object from a dictionary.
    Args:
        dict: dictionary of the general object.
        upacked_dict: the unpacked attributes of the general object.
        dict_class: dictionary of classes of interests.
    Returns:
        obj: the unpacked general object.
    """
    task = dict["deps"]["pipeline"]["kwargs"]["task"]
    # Use from_model_id api so that we don't have to explicitly instantiate hf's models and tokenizers
    return HuggingFacePipeline.from_model_id(
        model_id=dict["kwargs"]["model_id"],
        task=task,
        model_kwargs=dict["kwargs"]["model_kwargs"],
        device=0,
    )


def unpack_general(
    dict: Dict[str, Any], upacked_dict: Dict[str, Any], dict_class: Dict[str, Any]
) -> Any:
    """Unpack a general method object from a dictionary.
    Args:
        dict: dictionary of the general object.
        upacked_dict: the unpacked attributes of the general object.
        dict_class: dictionary of classes of interests.
    Returns:
        obj: the unpacked general object.
    """
    # Get the module and class name from the type string in the dict
    module_name = ".".join(dict["type"].split(".")[:-1])
    class_name = dict["type"].split(".")[-1]

    if class_name == "HuggingFacePipeline":
        return unpack_transformers_pipeline(dict, upacked_dict, dict_class)
    elif class_name in dict_class["list_class_transformers_pipeline"]:
        return dict

    # Import the module and class
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)

    # Get the list of arguments that the class needs
    argspec = inspect.getfullargspec(class_obj.__init__).args[1:]
    if argspec:
        upacked_dict = {k: v for k, v in upacked_dict.items() if k in argspec}

    # Create the class instance
    obj = class_obj(**upacked_dict)
    return obj


def _serialize(obj: Any, dict_class: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize an object into a dictionary.
    Args:
        obj: the object to be serialized.
        dict_class: dictionary of classes of interests.
    Returns:
        dict: the serialized dictionary.
    """

    # List obejcts need some special treatment
    if isinstance(obj, list):
        if is_list_of_strings(obj):
            # Return the list of strings directly
            return obj
        else:
            # Recursively serialize the objects in the list if they are not strings
            return [_serialize(item, dict_class) for item in obj]

    obj_type = str(type(obj))[8:-2]

    # patch name of the source script to the custom classes, otherwise can't be imported during unpack
    if obj_type in dict_class["list_class_custom"]:
        obj_type = os.environ["SOURCE_NAME"] + "." + obj_type

    # deps: attributes that are in the dict_class["list_class"] that need special instantiation (including langchain objects and custom objects)
    # kwargs: json serializable attributes that are not in the list_class
    obj_dict = {"type": obj_type, "deps": {}, "kwargs": {}}

    # Serialize each attribute of the object
    for key, value in vars(obj).items():
        type_name = str(type(getattr(obj, key)))[8:-2]

        if not type_name == "NoneType":
            type_name = type_name.split(".")[-1]

        if type_name not in dict_class["list_class"]:
            # Direclty save the attribute if it is not listed as a candidate for deps, and can be json serialized
            # Notice we do not save the API keys
            if is_json_serializable(value) and key not in LIST_API_KEYS:
                obj_dict["kwargs"][key] = value
            else:
                print(
                    f"WARNING: {obj_type} . {type_name} not in list_class and not JSON"
                    " serializable"
                )
            continue

        if isinstance(value, (list, tuple)):
            # Deal with the case where the attribute is a list of objects
            if is_json_serializable(value):
                obj_dict["kwargs"][key] = value
            else:
                obj_dict["deps"][key] = _serialize(value, dict_class)
        else:
            # Deal with the case where the attribute is a single object
            pack_func = map_type_to_pack[get_type(type_name, dict_class)]
            obj_packed = pack_func(value, dict_class)
            if obj_packed:
                obj_dict["deps"][key] = obj_packed

    return obj_dict


def _deserialize(dependency_dict: Any, dict_class: Type[Dict]) -> Any:
    """
    Deserialize a dependency dict to a Python object.

    Args:
        dependency_dict: A dictionary containing dependency information.
        dict_class: The dictionary class to use when deserializing.

    Returns:
        The deserialized object.
    """
    if not dependency_dict:
        return None

    # For lists and tuples, we recursively deserialize each item.
    if isinstance(dependency_dict, (list, tuple)):
        objs = []
        for item in dependency_dict:
            objs.append(_deserialize(item, dict_class))
        return objs

    # As for an individual object, we first deserialize its attributes listed under the "deps" key.
    deps = {}
    for key, value in dependency_dict["deps"].items():
        deps[key] = _deserialize(value, dict_class)

    # We then reinstantiate the object using its unpack method, deserialized attributes and other kwargs.
    obj_type = dependency_dict["type"]
    unpack_func = map_type_to_unpack[get_type(obj_type, dict_class)]
    obj = unpack_func(
        dependency_dict, {**deps, **dependency_dict["kwargs"]}, dict_class
    )

    return obj


def _package(
    app: Dict,
    app_name: str,
    script_path: str,
    lib_module_path: str,
) -> str:
    """Package the app into a directory.
    Args:
        app: the app to be packaged.
        app_name: the name of the app.
        script_path: the path to the script.
        lib_module_path: the path to the lib module.
    Returns:
        str: the path to the packaged app.
    """
    # Create the app directories
    os.environ["APP_DIR"] = "apps/{}_{}".format(
        app_name, time.strftime("%Y%m%d-%H%M%S")
    )

    delete_and_create_dir(os.environ["APP_DIR"])
    delete_and_create_dir(os.environ["STATIC_DIR"])
    delete_and_create_dir(os.environ["MEMORY_DIR"])

    with open("app.json", "w", encoding="utf-8") as json_file:
        json.dump(app, json_file, indent=4)

    # Copy templates into the app and replace the placeholders
    # Modify the copies based on the app
    replace_word_in_file("app.json", "__main__", lib_module_path)

    spec = importlib.util.find_spec("langpack")
    langpack_path = os.path.dirname(spec.origin)

    # chatbot-ui backend
    chatbot_ui_backend_template_path = (
        os.path.abspath(langpack_path) + "/chatbot_ui_backend_template.py"
    )
    chatbot_ui_backend_py_path = os.path.join(
        os.environ["APP_DIR"], "chatbot_ui_backend.py"
    )
    shutil.copy2(chatbot_ui_backend_template_path, chatbot_ui_backend_py_path)

    # slack backend
    slack_backend_template_path = (
        os.path.abspath(langpack_path) + "/slack_backend_template.py"
    )
    slack_backend_py_path = os.path.join(os.environ["APP_DIR"], "slack_backend.py")
    shutil.copy2(slack_backend_template_path, slack_backend_py_path)

    # Simple Flask backend
    app_template_path = os.path.abspath(langpack_path) + "/app_template.py"
    app_py_path = os.path.join(os.environ["APP_DIR"], "app.py")
    shutil.copy2(app_template_path, app_py_path)

    client_template_path = os.path.abspath(langpack_path) + "/client_template.py"
    client_py_path = os.path.join(os.environ["APP_DIR"], "client.py")
    shutil.copy2(client_template_path, client_py_path)

    index_template_path = os.path.abspath(langpack_path) + "/index.html"
    index_path = os.path.join(os.environ["STATIC_DIR"], "index.html")
    shutil.copy2(index_template_path, index_path)

    input_key = None
    output_key = None

    if app["dependency_dict"]["type"].split(".")[-1] == "AgentExecutor":
        input_key = '"input"'
        output_key = '"output"'
    elif app["dependency_dict"]["type"].split(".")[-1] == "BabyAGI":
        input_key = '"objective"'
        output_key = '"output"'
    else:
        if "input_key" in app["dependency_dict"]["kwargs"]:
            input_key = '"' + app["dependency_dict"]["kwargs"]["input_key"] + '"'
        elif "question_key" in app["dependency_dict"]["kwargs"]:
            input_key = '"' + app["dependency_dict"]["kwargs"]["question_key"] + '"'
        else:
            print("can't find input_key for app")

        if "output_key" in app["dependency_dict"]["kwargs"]:
            output_key = '"' + app["dependency_dict"]["kwargs"]["output_key"] + '"'
        else:
            print("can't find output_key for app")

    if input_key:
        replace_word_in_file(app_py_path, '{"input_key"}', input_key)
        replace_word_in_file(client_py_path, '{"input_key"}', input_key)
        replace_word_in_file(index_path, "$input_key$", input_key)
    if output_key:
        replace_word_in_file(app_py_path, '{"output_key"}', output_key)
        replace_word_in_file(client_py_path, '{"output_key"}', output_key)
        replace_word_in_file(index_path, "$output_key$", output_key)

    app_script_path = os.path.join(os.environ["APP_DIR"], script_path)
    shutil.copy2(script_path, app_script_path)

    shutil.move(lib_module_path + ".py", os.environ["APP_DIR"])

    init_path = os.path.join(os.environ["APP_DIR"], "__init__.py")
    with open(init_path, "w", encoding="utf-8") as _:
        pass

    if os.path.exists(os.environ["VECTORSTORE_DIR"]):
        shutil.move(os.environ["VECTORSTORE_DIR"], os.environ["APP_DIR"])
    shutil.move(os.environ["STATIC_DIR"], os.environ["APP_DIR"])
    shutil.move(os.environ["MEMORY_DIR"], os.environ["APP_DIR"])

    shutil.move("app.json", os.environ["APP_DIR"])

    # print success msg and test command
    output_path = os.path.join(os.getcwd(), os.environ["APP_DIR"])
    print_success(output_path)
    return output_path


# Mapping from type name to pack/unpack functions.
map_type_to_pack = {
    "chain": pack_general,
    "agent": pack_general,
    "embedding": pack_general,
    "memory": pack_general,
    "request_wrapper": pack_general,
    "tool": pack_general,
    "vectorstore": pack_general,
    "prompt": pack_general,
    "llm": pack_general,
    "custom": pack_general,
    "chatmodel": pack_general,
    "index": pack_general,
    "docstore": pack_general,
    "function": pack_function,
    "method": pack_method,
    "utility": pack_general,
    "transformers_pipeline": pack_general,
}


map_type_to_unpack = {
    "chain": unpack_general,
    "agent": unpack_general,
    "embedding": unpack_embedding,
    "memory": unpack_general,
    "request_wrapper": unpack_general,
    "tool": unpack_general,
    "vectorstore": unpack_vectorstore,
    "prompt": unpack_general,
    "llm": unpack_general,
    "custom": unpack_general,
    "chatmodel": unpack_general,
    "index": unpack_general,
    "docstore": unpack_general,
    "function": unpack_function,
    "method": unpack_method,
    "utility": unpack_general,
    "transformers_pipeline": unpack_general,
}
