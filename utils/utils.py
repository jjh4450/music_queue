import random
from typing import List, Any

def shuffle_list(items: List[Any]) -> List[Any]:
    """
    주어진 리스트를 무작위로 셔플한 뒤 반환합니다.

    :param items: 셔플할 리스트
    :return: 셔플된 리스트
    """
    new_items = items[:]
    random.shuffle(new_items)
    return new_items
