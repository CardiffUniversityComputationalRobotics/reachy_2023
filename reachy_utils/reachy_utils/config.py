from functools import partial
import yaml
import os
from launch_ros.substitutions import FindPackageShare

reachy_utils_dir = FindPackageShare(package="reachy_utils").find("reachy_utils")
config_file = os.path.expanduser(reachy_utils_dir + "/.reachy.yaml")


def get_reachy_config():
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config


def _get_config_parameter(parameter: str, part=None):
    config = get_reachy_config()
    try:
        return config[parameter]
    except KeyError:
        print(f"{parameter} not found in {config_file}")
        return -1


get_reachy_generation = partial(_get_config_parameter, "generation")
get_reachy_model = partial(_get_config_parameter, "model")
get_reachy_serial_number = partial(_get_config_parameter, "serial_number")
get_zuuu_version = partial(_get_config_parameter, "zuuu_version")
get_neck_orbita_zero = partial(_get_config_parameter, "neck_orbita_zero")
get_camera_parameters = partial(_get_config_parameter, "camera_parameters")
get_fan_trigger_temperature = partial(_get_config_parameter, "fan_trigger_temperature")
