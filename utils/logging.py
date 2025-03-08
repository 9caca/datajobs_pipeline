import logging
import os

def setup_logging():
    logging.basicConfig(
        filename="utils/datajobs_pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a",
        force=True
    )
