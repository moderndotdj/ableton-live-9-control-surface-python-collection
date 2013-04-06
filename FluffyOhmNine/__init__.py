# http://aumhaa.blogspot.com

from FluffyOhmNine import FluffyOhmNine

def create_instance(c_instance):
    """ Creates and returns the OhmModes script """
    return FluffyOhmNine(c_instance)

from _Framework.Capabilities import *


def get_capabilities():
    return {
        CONTROLLER_ID_KEY: controller_id(vendor_id = 9876, product_ids = [
            77], model_name = 'Livid OhmRGB'),
        PORTS_KEY: [
            inport(props = [
                NOTES_CC,
                SCRIPT,
                REMOTE]),
            outport(props = [
                SCRIPT,
                REMOTE])] }
