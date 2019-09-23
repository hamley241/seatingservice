import os
import yaml
from collections import OrderedDict
import logging

class Config:
    __data_map = None
    __custom_stop_words = None
    __zonal_dict = None

    @staticmethod
    def get_data_map():
        file_name = "config.yaml"
        input_file = os.path.dirname(os.path.realpath(__file__))+"/../config/" + file_name
        if not Config.__data_map:
            logging.error("loaded config file")
            logging.error(input_file)
            Config.__data_map = Config.__ordered_load(open(input_file), yaml.SafeLoader)
        return Config.__data_map

    @staticmethod
    def __ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
        class OrderedLoader(Loader):
            pass

        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))

        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(stream, OrderedLoader)




if __name__ == "__main__":
    cfg = Config().get_data_map()
    print(cfg.get("theatre").get("default").get("seats_matrix")[0].get("name"))