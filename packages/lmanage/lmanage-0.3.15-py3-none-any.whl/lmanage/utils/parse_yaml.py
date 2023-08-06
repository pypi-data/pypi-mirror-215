import json
import ruamel.yaml 
import logging
from lmanage.utils import logger_creation as log_color

#logger = log_color.init_logger(__name__, logger_level)




class Yaml:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        with open(self.yaml_path, 'r') as file:
            self.parsed_yaml = yaml.load(file, Loader=yaml.BaseLoader)

    def get_permission_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'permissions' in list(objects.keys()):
                response.append(objects)
        response = [r for r in response if r.get('name') != 'Admin']
        return response

    def get_model_set_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'models' in list(objects.keys()):
                response.append(objects)
        return response

    def get_role_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'permission_set' and 'model_set' in list(objects.keys()):
                response.append(objects)
        response = [r for r in response if r.get('name') != 'Admin']
        return response

    def get_folder_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'content_metadata_id' in list(objects.keys()):
                response.append(objects)
        return response

    def get_user_attribute_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'hidden_value' in list(objects.keys()):
                response.append(objects)
        return response

    def get_look_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'query_obj' in list(objects.keys()):
                response.append(objects)
        return response
    
    def get_dash_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'lookml' in list(objects.keys()):
                response.append(objects)
        return response

    def get_board_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'board_sections' in list(objects.keys()):
                response.append(objects)
        return response
