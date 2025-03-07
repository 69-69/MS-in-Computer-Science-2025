# static/error_handler.py

import logging
import inspect
from flask import flash


class ErrorHandler:
    def __init__(self):
        # Setup logger
        self.logger = logging.getLogger('ErrorHandler')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)

    def _get_error_details(self):
        """Helper method to fetch the file and line number from the stack."""
        try:
            stack = inspect.stack()

            # Ensure the stack has enough frames to access the calling function
            if len(stack) < 3:
                raise IndexError("Stack does not have enough frames to determine the caller details.")

            # stack[2] is the caller of the function that called _get_error_details
            filename = stack[2].filename  # The calling function's filename
            line_number = stack[2].lineno  # The calling function's line number

            return filename, line_number

        except IndexError:
            return "Unknown", -1  # Return unknown file and line number in case of error

    def _log_error(self, message):
        """Helper method to log the error."""
        self.logger.error(message)

    def handle_config(self, exception, context=""):
        """Handles exception for Config class and returns a consistent error message."""
        flash(str(exception), 'error')

        # Make sure to call this method from an instance of ErrorHandler
        filename, line_number = self._get_error_details()
        error_message = f"Error occurred in file: {filename}, line: {line_number}. \n{exception}"

        if context:
            error_message = f"{context}: {error_message}"

        # Log the error
        self._log_error(self.display_style(error_message, "CONFIG"))

        # Optionally log the stack trace (uncomment if needed)
        # self._log_error(f"Stack trace:\n{traceback.format_exc()}")

        # Return standardized error message
        return error_message

    def handle_controller(self, exception):
        """Handles exception for Controller and returns success flag and error message."""

        # Make sure to call this method from an instance of ErrorHandler
        filename, line_number = self._get_error_details()
        error_message = f"Error occurred in file: {filename}, line: {line_number}. \n{exception}"

        # Log the error
        self._log_error(self.display_style(error_message, "CONTROLLER"))

        # Optionally log the stack trace (uncomment if needed)
        # self._log_error(f"Stack trace:\n{traceback.format_exc()}")

        # Return failure status and error message
        return False, self.display_style(error_message, "CONTROLLER")

    def display_style(self, error_message, dir):
        return f"\n********:: ( CS-7330 GROUP-11 ) FROM { dir } ERROR ::********\n" \
               f"{error_message}" \
               f"\n********:: END { dir } ERROR ::********\n\n"
