import logging
import json
import argparse
from ingestion.meta_interface import MetaITF


class CommandITF(argparse.Action):
    def __init__(self, option_strings, logger: logging.Logger, properties: json, purpose: str, *args, **kwargs):
        super(CommandITF, self).__init__(option_strings, *args, **kwargs)
        self.log = logger
        self.prop = properties
        self.purpose = purpose

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        #print('[Debug2]:',self, parser, namespace, values, option_string)
        self.log.info(f"{self.purpose=}")
        self.log.info(vars(namespace))
        meta_interface = MetaITF(self.log, self.prop)
        attr_function = getattr(meta_interface, self.purpose)
        #print('[Debug3]:',values)
        #print('[Debug3-1]:',vars(namespace))
        if len(vars(namespace)) < 2:
            attr_function(values)
        else:            
            attr_function(vars(namespace))

