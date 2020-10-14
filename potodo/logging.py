import logging


def setup_logging(logging_level: int) -> None:
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s %(levelname)-8s [%(filename)s:"
        "%(lineno)d %(funcName)s()] %(message)s",
        datefmt="%d-%m-%Y:%H:%M:%S",
    )
    # Silencing some loggers
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
