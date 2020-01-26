from datetime import datetime, timezone
from typing import Union, List, Dict
from numpy import array, ndarray


class Data:
    def __init__(self, data_type: str, value: Union[float, array, List] = None,
                 timestamp: datetime = datetime.now(timezone.utc)):
        self.data_type: str = data_type
        if str(type(value)).split("'")[1] == 'float':
            self.value: int = value
        self.value: ndarray = array(value)
        self.timestamp: datetime = timestamp


def serialise(data: Data) -> Dict:
    print(data.value)
    data_as_dict: Dict = {
        "data_type": data.data_type,
        "timestamp": datetime.strftime(data.timestamp, "%Y-%m-%d-%H-%M-%S-%z"),
        "value": list(data.value)
    }

    print(str(type(data.value)).split("'")[1])
    return data_as_dict


def serialise_many(data: List) -> List:
    data_as_list: List = []

    for i in data:
        data_as_list.append(serialise(i))

    return data_as_list


def deserialise(data_as_dict: Dict) -> Data:
    data_as_dict["timestamp"] = datetime.strptime(data_as_dict["timestamp"], "%Y-%m-%d-%H-%M-%S-%z")

    data: Data = Data(data_as_dict["data_type"], data_as_dict["value"], data_as_dict["timestamp"])

    return data


def deserialise_many(data_as_list: List) -> Data:
    list_of_data: List = []

    for data_as_dict in data_as_list:
        list_of_data.append(deserialise(data_as_dict))

    return list_of_data
