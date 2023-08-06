import json
import os
from qashared.models.extensions.divido_simple_namespace import DividoSimpleNamespace
import inspect

def get_variable_name(var: any) -> str:
    """Gets the name of the variable, for more informative errors 

    Args:
        var (any): The variable 

    Returns:
        str: The name of the variable, or "unknown" if it can't be found
    """    
    # todo improve
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    var_list = [var_name for var_name, var_val in callers_local_vars if var_val is var]

    if len(var_list) == 0:
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        var_list = [var_name for var_name, var_val in callers_local_vars if var_val is var]

    return var_list[0] if len(var_list) > 0 else "unknown"

def update_config_with_env_vars(config: dict, env_key_prefix='') -> dict:
    """Updates a config dict with environment variables if they exist, using either . or __ to denote child elements

    Args:
        config (dict): The config to be overridden 
        env_key_prefix (str, optional): An optional prefix to filter environment variables. Defaults to ''.

    Returns:
        dict: The config with overridden values for any environment variables found
    """    
    for key in config:
        env_key = f"{env_key_prefix}{key}"
        if env_key in os.environ:
            config[key] = os.environ[env_key]
    
        if isinstance(config[key], dict):
            update_config_with_env_vars(config[key], env_key_prefix=f"{env_key}.")
            update_config_with_env_vars(config[key], env_key_prefix=f"{env_key}__")

    return config

def load_config() -> DividoSimpleNamespace:
    """ 1) Loads the local config into a DividoSimpleNamespace object, using first 'config.local.json' then 'config.json'
        2) Overrides values if relevant environment variables exist 

    Returns:
        DividoSimpleNamespace: An object representing the config data 
    """    
    path = 'config.local.json' if os.path.isfile('config.local.json') else 'config.json'
    with open(path, 'r') as f:
        config = json.load(f)

    config = update_config_with_env_vars(config)
    return json.loads(json.dumps(config), object_hook=lambda d: DividoSimpleNamespace(**d))

def get_object_from_dict(dict: dict) -> DividoSimpleNamespace:
    """Converts a dict into a DividoSimpleNamespace

    Args:
        dict (dict): The dict to convert 

    Returns:
        DividoSimpleNamespace: The object representing the provided dict 
    """    
    return json.loads(json.dumps(dict), object_hook=lambda d: DividoSimpleNamespace(**d))

def add_test_data_from_files(data: DividoSimpleNamespace, directory='./data') -> DividoSimpleNamespace:
    """Updates an existing DividoSimpleNamespace with json data stored in a given directory

    Args:
        data (DividoSimpleNamespace): The existing object 
        directory (str, optional): The data directory. Defaults to './data'.

    Returns:
        DividoSimpleNamespace: The existing object, now updated with the local json data 
    """    
    checklist = []
    for root, dirs, files in os.walk(directory):
        for file in files: 
            with open(os.path.join(root, file)) as f:
                json_data = json.load(f)
            data_obj = get_object_from_dict(json_data)
            
            formatted_root = root.replace('./', '').replace('/', '.')
            formatted_file = file.replace('.json', '')
            formatted_directory = f"{directory.replace('./', '').replace('/', '.')}."
            
            attribute_str = f'{formatted_root}.{formatted_file}'.replace(formatted_directory, '')
            checklist.append(attribute_str)
            
            attributes = []
            for i in attribute_str.split('.'):
                if data.get_attribute_or_none(i) is None:
                    obj = data
                    for parent in attributes:
                        obj = obj.__getattribute__(parent)
                    
                    obj.__setattr__(i, DividoSimpleNamespace())
                    attributes.append(i)
                    
            leaf_obj = data
            for attribute in attributes:
                leaf_obj = leaf_obj.__getattribute__(attribute)
                
            leaf_obj.__setattr__('as_json', json_data)
            leaf_obj.__setattr__('as_object', data_obj)
                     
    data.verify_attributes(checklist, 'Test data object not set up correctly, there were the following missing attributes')  
    return data
