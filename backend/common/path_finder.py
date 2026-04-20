# acess paths of modules
from os.path import sep

from backend.config import path


def path_algorithms(module):
    return path + sep + "algorithms" + sep + module + sep


def path_datasets(module):
    return path + sep + "datasets" + sep + module + sep


def path_log(module):
    return path + sep + "log" + sep + module + sep


def path_services(module):
    return path + sep + "services" + sep + module + sep


# def path_test(module):
#     return path + sep + "test" + sep + module + sep
#

