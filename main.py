from src.utils import (
    Parts,
    build_longest_chain,
    fill_part_matches,
    load_data,
    merge_chain,
    remove_part_without_match,
    setup_logger,
    save_result,
    )


def main(path_to_file: str) -> None:
    """
    Performs the process of finding the longest chain of parts in a file.

    param path_to_file (str): Path to the text file with the source data
    """
    logger = setup_logger()
    logger.info("Start finding the longest chain")

    try:
        data_list = load_data(path_to_file)
        logger.info(f"file '{path_to_file}' loaded,"
                    f" with {len(data_list)} elements")
    except FileNotFoundError:
        logger.error(f"FileNotFoundError: file {path_to_file} not found")
        raise
    except Exception as err:
        logger.exception("Unexpected error:\n"
              f"file {path_to_file}\n{err}")
        raise

    # Initialize Parts and prepare them for chain search
    parts = [Parts(item) for item in data_list]
    fill_part_matches(parts, logger)

    # If an element has no matches from the head and tail, it is removed.
    original_parts = parts.copy()
    remove_part_without_match(parts, logger)
    if not parts:
        logger.warning("All parts were removed after filtering. "
                       "Using original list")
        parts = original_parts

    best_chain = build_longest_chain(parts, logger)
    result = merge_chain(best_chain)

    logger.info(f"A string of {len(best_chain)} elements was found\n"
        f"\t\t\t\tTotal length of the string {len(result.value)} characters\n"
        f"\t\t\t\t{result.value}")

    try:
        save_result(result.value, logger)
    except (TypeError, OSError):
        logger.error("Failed to save result")

    logger.info(f"Finish finding the longest chain")


if __name__ == "__main__":
    path_to_file = "data/source2.txt"
    main(path_to_file)
