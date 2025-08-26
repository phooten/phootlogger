################################################################################
#
# Filename: logger.py
#
# Purpose:  Class create a logger and use generally across many python projects
#
################################################################################

# External imports
from typing import Tuple
import datetime
import inspect
import os

# Internal import
from phootlogger.report import Report
from phootlogger.message_builder import MessageBuilder


################################################################################
class Logger:
    """!
    @brief      This class can be instantiated in a python project and report
                consistent logs with timestamps, function names, and classes
    """
    # --------------------------------------------------------------------------
    def __init__(self):
        # Set up default log format
        self.mb = MessageBuilder()
        self.mb.set_hide_source(False)
        self.mb.set_hide_timestamps(False)
        self.mb.set_hide_owner(True)

        # Setting up logger flags
        self._debug_mode = False

        # Setup owner file
        self.set_owner_filepath()

    # --------------------------------------------------------------------------
    def set_owner_filepath(self) -> None:
        """!
        @brief      Determines the file path of where this logger was instantiated.
                    Values is set internally to this class
        """
        # Determine the file that initialized the logger
        frame_info = inspect.stack()[1]
        filepath = frame_info.filename
        self.owner_filepath = os.path.abspath(filepath)

    # --------------------------------------------------------------------------
    def info(self, msg) -> None:
        """
        @brief      Prints out Informational message to the user

        @param      msg (string): Message to be printed out to user
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        # Try to print the messages
        if not self._print_user_message("INFO", msg, ts):
            print("Issue with INFO log.")
            self.quit_script()

    # --------------------------------------------------------------------------
    def warning(self, msg) -> None:
        """!
        @brief      Prints out warning message to the user

        @param      msg (string): Message to be printed out to user
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        if not self._print_user_message("WARNING", msg, ts):
            print("Issue with WARNING log.")
            self.quit_script()

    # --------------------------------------------------------------------------
    def error(self, msg) -> None:
        """
        @brief      Prints out Error message to the user

        @param      msg (string): Message to be printed out to user
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        if not self._print_user_message("ERROR", msg, ts):
            print("Issue with ERROR log.")
            self.quit_script()

    # --------------------------------------------------------------------------
    def debug(self, msg) -> None:
        """!
        @brief      Prints out debug message to the user. This is only shown
                    when the logger is set to debug mode

        @param      msg (string): Message to be printed out to user
        """
        if self._debug_mode:
            # Get time stamp as soon as this is called
            ts = self._get_time_stamp()

            if not self._print_user_message("DEBUG", msg, ts):
                print("Issue with DEBUG log.")
                self.quit_script()

    # --------------------------------------------------------------------------
    def quit_script(self) -> None:
        """!
        @brief  Will print a message and ungracefully exit with 1
        """
        print("Exiting script.")
        exit(1)

    # --------------------------------------------------------------------------
    def set_debug_mode(self, debug_mode=True) -> None:
        """!
        @brief  When enabled, will print out debugging messages

        @param  debug_mode (bool): State to set the debug mode to. ( True = Debug, False = No debug )
        """
        self._debug_mode = debug_mode

    # --------------------------------------------------------------------------
    def hide_logs_timestamps(self, hide_timestamps=False) -> None:
        """!
        @brief  Will show or hide the timestamps printed out based on this state
        """
        self.mb.set_hide_timestamps(hide_timestamps)

    # --------------------------------------------------------------------------
    def hide_logs_source(self, hide_source=False) -> None:
        """!
        @brief  Will show or hide the source ( class / method names) printed out
                based on this state
        """
        self.mb.set_hide_source(hide_source)

    # --------------------------------------------------------------------------
    def hide_logs_owner(self, hide_owner=True) -> None:
        """!
        @brief  Will show or hide the file that owns the log instantiation,
                printed out based on this state
        """
        self.mb.set_hide_owner(hide_owner)

    # --------------------------------------------------------------------------
    def _get_caller_context(self) -> Tuple[str, str]:
        """!
        @brief      Extract the calling class and method name

        @returns    Tuple:  class_name(str):  Name of the class calling the log
                            method_name(str): Name of the method calling the log
        """
        frame = inspect.currentframe()
        logger_class = self.__class__

        # Track frames back to the caller
        while frame:
            frame = frame.f_back
            if not frame:
                break

            # Skip frames from within the logger class
            if 'self' in frame.f_locals:
                caller_self = frame.f_locals['self']
                if isinstance(caller_self, logger_class):
                    continue
                class_name = caller_self.__class__.__name__
            else:
                class_name = None

            method_name = frame.f_code.co_name
            return class_name, method_name

        # Print a warning
        if not method_name or not class_name:
            print("WARNING. Method name or Class name not found from logger.")

        return class_name, method_name

    # --------------------------------------------------------------------------
    def _print_user_message(self, message_type: str, message_to_user: str, time_stamp: str) -> bool:
        """!
        @brief      Prints out the message after everything is set

        @param      message_type (str): Type of message to be displayed.
                                        i.e. "ERROR", "INFO", "DEBUG", etc.
        @param      message_to_user (str): Message to be directly displayed to the user
        @param      time_stamp (str): Time stamp of the message

        @retval     True:   Always
        @retval     False:  Never
        """
        # Get the calling methods
        class_name, method_name = self._get_caller_context()

        # Build the string
        formatted_message = self.mb.build_log_string(time_stamp=time_stamp,
                                                     owner=self.owner_filepath,
                                                     class_name=class_name,
                                                     method_name=method_name,
                                                     message_type=message_type,
                                                     message_to_user=message_to_user)

        print(formatted_message)
        return True

    # --------------------------------------------------------------------------
    def _get_time_stamp(self) -> str:
        """!
        @brief      Gets the current time

        @returns    (str): Current time in the format: 'YYYY-mm-DD HH:MM:SS.ssssss'
        """
        current_time = str(datetime.datetime.now())
        return current_time


    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!! START OF DEPRECATION WARNING SECTION
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # NOTE: Keeping this here for use next time deprecation is required. I might
    #       consider using an external library or making my own for this.
    # --------------------------------------------------------------------------
    def _deprecation_warning(self, immediate=False):
        """!
        @brief      Notify users this method will be deprecated soon.
        """
        # Pass the soon or immediate deprecation
        time = "will soon"
        if immediate:
            time = "has been"

        # Determine the method and print out
        caller = inspect.stack()[1].function
        print(f"WARNING. The method '{caller}' {time} DEPRECATED.")

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!! END OF DEPRECATION WARNING SECTION
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


