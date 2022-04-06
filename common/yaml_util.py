import os
import traceback
import yaml

class YamlUtil:

    def read_yaml_file(self,yaml_name,part):
        with open(os.getcwd()+"/testdata/"+yaml_name, mode='r', encoding='utf-8') as f:
                value = yaml.load(stream=f, Loader=yaml.FullLoader)
                new_value = value[part]
                return new_value

