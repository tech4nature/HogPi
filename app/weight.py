import logging
from typing import Dict, List
from numpy import ndarray, sort, array, float
import json

from hx711 import HX711
import data

# TODO: Config
config: Dict = {
    "min_percentile": 75,
    "spike_cut": 5  # A percentage of values that will be cut off to get rid of spikes
}


logger = logging.getLogger(__name__)


class Sensor:
    def __init__(self):
        # Configure and initialise HX711

        self.hx: HX711 = HX711(5, 6)
        self.hx.set_reading_format("LSB", "MSB")
        self.hx.set_reference_unit(398)  # TODO: Make Calibration Script
        self.hx.reset()
        
    def tare_weight(self) -> None:
        old_offset = self.hx.OFFSET
        self.hx.tare()
        new_offset = self.hx.OFFSET
        diff = old_offset - new_offset

        if (diff < -50 or diff > 50) and old_offset != 1:
            self.hx.OFFSET = old_offset
    
    def read(self, times: int = 10) -> data.Data:
        # Read and refine weight

        weights: List = []

        for i in range(times):
            weight: float = self.hx.get_weight()

            if weight < 0:
                weight: float = 0

            weight: float = float('%.2f' % weight)
            weights.append(weight)

        logger.debug(weights)
        print(weights)
        weights: ndarray = array(weights).astype(float)
        weight: data.Data = data.Data("weight", weights)

        return weight

    @staticmethod
    def avrg(weight: data.Data) -> data.Data:
        weights: ndarray = weight.value
        weights: ndarray = sort(weights)

        print(weights)
        weights: ndarray = weights[:int((len(weights)/100)*(100-config["spike_cut"]))]
        print(weights)
        max_value: float = weights[-1]
        min_cut: float = (max_value / 100) * config["min_percentile"]
        weights: ndarray = weights[weights > min_cut]
        print(weights)

        final_weight = data.Data(weight.data_type, [float('%.2f' % weights.mean())], weight.timestamp)

        data_as_dict: Dict = data.serialise(final_weight)
        weights_dict: List = json.load(open("weight.json", "r"))
        weights_dict.append(data_as_dict)
        json.dump(weights_dict, open("weight.json", "w"))

        return final_weight



