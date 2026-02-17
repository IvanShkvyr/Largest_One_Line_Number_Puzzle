import copy
import logging
from pathlib import Path
from typing import List, Dict


LOGGER_LEVEL = logging.DEBUG
LOGGER_NAME = "chain"


class Parts:
    def __init__(self, value: str):
        self.value = value
        self.head = value[:2]
        self.tail = value[-2:]
        self.match_head = set()
        self.match_tail = set()


def load_data(path_to_file: str) -> List[str]:
    """
    Load data from a file.
    """
    data_list = []

    with open(path_to_file, "r") as data:
        for line in data:
            data_list.append(line.strip())

    return data_list


def setup_logger(
        logger_level: int = LOGGER_LEVEL,
        log_name: str = LOGGER_NAME,
        ) -> logging.Logger:
    """
    Configurate and return a logger that logs message to a console.
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(logger_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def create_index(parts: List[Parts], atr: str) ->  Dict[str, List[Parts]]:
    """
    Creates dictionaries with part indexes by attribute.
    """
    index_dict = {}

    for part in parts:
        atr_value = getattr(part, atr)
        index_dict.setdefault(atr_value, []).append(part)

    return index_dict


def fill_match_by_attribute(
                            parts: List[Parts],
                            index_dict: Dict[str, List[Parts]],
                            atr: str,
                            match_atr: str
                            ) -> None:
    """
    Populates the set of related instances for each instance of the class.
    """
    for part in parts:
        atr_value = getattr(part, atr)
        if atr_value not in index_dict:
            continue

        match_atr_value = getattr(part, match_atr)
        for matched_part in index_dict[atr_value]:
            if matched_part is not part:
                match_atr_value.add(matched_part)


def get_start_parts(parts: Parts, logger: logging.Logger) -> List[Parts]:
    """
    Selects the start elements for a sequence.
    """
    start_parts = [p for p in parts if not p.match_head]

    if not start_parts:
        logger.warning("No starting parts found (all elements have match_head)."
                        f"Using all {len(parts)} parts as starts.")
        start_parts = parts

    logger.info(f"{len(start_parts)} elements were found that could be the "
                "beginning of the sequence")

    return start_parts


def explore_chain(
                part: Parts,
                best_chain: list,
                visited: set = set(), 
                chain: List[Parts] = [],
                ) -> None:
    """
    Recursive function to build the longest chain.
    """
    visited.add(part)
    chain.append(part)

    if len(chain) > len(best_chain):
        best_chain.clear()
        best_chain.extend(chain)

    for next_part in part.match_tail:
        if next_part not in visited:

            explore_chain(next_part, best_chain, visited, chain,)

    visited.remove(part)
    chain.pop()


def build_longest_chain(parts: List[Parts], logger: logging.Logger) -> Parts:
    """
    Building the longest chain of Parts objects.
    """
    start_parts = get_start_parts(parts, logger)
    best_chain = []

    for start in start_parts:
        explore_chain(start, best_chain)
        logger.info(f"All possible combinations with the initial"
                    f" element {start.value} are checked")

    return best_chain


def merge_parts(part_head: Parts, part_tail: Parts ) -> Parts:
    """
    Merges two instances of the Parts class. The value of the part_head
    object is added to the value of the part_tail object, and
    the part_head attributes tail and match_tail are overwritten with
    the values from part_tail.
    """
    part_head.value = part_head.value + part_tail.value[2:]
    part_head.tail = part_tail.tail
    part_head.match_tail = part_tail.match_tail

    return part_head


def merge_chain(chain: list[Parts]) -> Parts:
    """
    Combines all items in the Parts object list into a single object.
    """
    result = copy.deepcopy(chain[0])

    for next_part in chain[1:]:
        result = merge_parts(result, next_part)

    return result


def remove_part_without_match(
                            parts: List[Parts],
                            logger: logging.Logger
                            ) -> None:
    """
    Removes an item from the Parts object list if the item has no matches
    at either the head or end of the item.
    """
    copy_parts = parts[:]

    for part in copy_parts:
        if not part.match_tail and not part.match_head:
            parts.remove(part)

    if len(copy_parts) != len(parts):
        logger.info(f"{len(copy_parts) - len(parts)} elements that had "
                    "no connections to other elements were removed")
        

def fill_part_matches(parts: List[Parts], logger: logging.Logger) -> None:
    """
    Fills in the match_head and match_tail attributes in all instances of Parts
    in the list.
    """
    head_index = create_index(parts, "head")
    tail_index = create_index(parts, "tail")

    fill_match_by_attribute(parts, tail_index, "head", "match_head")
    fill_match_by_attribute(parts, head_index, "tail", "match_tail")

    logger.info("Head and tail indexes created")


def save_result(
                data: str,
                logger: logging.Logger,
                path: str = "longest_chain.txt"
                ) -> None:
    """
    Saves data to a file.
    """
    with open(path, "w") as f:
        f.write(data)

    logger.info(f"The longest chain was saved to file {path}")
