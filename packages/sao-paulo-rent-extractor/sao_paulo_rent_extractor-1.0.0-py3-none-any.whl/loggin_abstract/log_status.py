import logging
import inspect

def logger(message, status='INFO', filename=None):
    # Get the caller's frame information
    if filename is None:
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
    line_number = frame.f_lineno

    # Configure the logging format
    logging.basicConfig(format='%(asctime)s | %(levelname)s | %(lineno)d | %(filename)s | %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    # Create a logger and log the message
    logger = logging.getLogger(__name__)
    getattr(logger, status.lower())(message)

# Usage example
# custom_logger("This is an information message", status="INFO", filename=__file__)
