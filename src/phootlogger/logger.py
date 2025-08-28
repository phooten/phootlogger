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
import sys

# Internal import
from phootlogger.report import Report
from phootlogger.message_builder import MessageBuilder


################################################################################
class Logger:
    """!
    @brief      This class can be instantiated in a python project and report
                consistent logs with timestamps, function names, and classes
    """

    # Singleton instance
    _instance = None
    _initialized = False
    _program_name = "LOGGER"

    # --------------------------------------------------------------------------
    def __new__(cls):
        """!
        @brief      Ensures only one instance of Logger exists ( singleton pattern )
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    # --------------------------------------------------------------------------
    def __init__(self):
        # Prevent re-initialization if already initialized
        if self._initialized:
            return

        # Setting up logger flags
        self._debug_mode = False
        self._report_enabled = False

        # Configure Logger
        self.report = Report(self._program_name)
        self.enable_report()

        self.mb = MessageBuilder()
        self.hide_logs_source(False)
        self.hide_logs_timestamps(False)
        self.hide_logs_calling_file(True)

        # # Register cleanup to run at program exit
        # import atexit
        # atexit.register(self.cleanup)

        # # Register signal handlers for graceful shutdown
        # import signal
        # signal.signal(signal.SIGINT, self._signal_handler)
        # signal.signal(signal.SIGTERM, self._signal_handler)

        # Mark as initialized
        self._initialized = True

    # --------------------------------------------------------------------------
    # def _signal_handler(self, signum, frame):
    #     """!
    #     @brief      Handle interrupt signals gracefully
    #     """
    #     self.info(f"Received signal {signum}, cleaning up...")
    #     self.cleanup()
    #     sys.exit(0)

    # --------------------------------------------------------------------------
    def __enter__(self):
        """!
        @brief      Context manager entry point
        """
        return self

    # --------------------------------------------------------------------------
    def __del__(self):
        # Don't call complex operations in __del__ as built-ins may not be available
        # Use manual cleanup instead. This is a limitation in python
        pass

    # --------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_val, exc_tb):
        """!
        @brief      Context manager exit point - ensures cleanup
        """
        self.cleanup()

    # --------------------------------------------------------------------------
    def cleanup(self):
        """!
        @brief      Manually cleanup and save report before destruction
                    Call this method explicitly instead of relying on __del__
        """

        if self._report_enabled:
            success = self._save_report()
            if not success:
                self.error("No report saved during cleanup.")
                return

            self.info("Report successfully saved during cleanup.")
        else:
            self.info("Report not enabled. Not saving log file.")


    # --------------------------------------------------------------------------
    @classmethod
    def configure(cls, program_name: str):
        cls._program_name = program_name

    # --------------------------------------------------------------------------
    @classmethod
    def get_instance(cls):
        """!
        @brief      Intended to call "__new__" / get the singleton instance
        """
        return cls()

    # --------------------------------------------------------------------------
    def info(self, msg) -> None:
        """
        @brief      Prints out Informational message to the user

        @param      msg (string): Message to be printed out to user
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        # Try to print the messages
        if not self._log_user_method("INFO", msg, ts):
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

        if not self._log_user_method("WARNING", msg, ts):
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

        if not self._log_user_method("ERROR", msg, ts):
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

            if not self._log_user_method("DEBUG", msg, ts):
                print("Issue with DEBUG log.")
                self.quit_script()

    # --------------------------------------------------------------------------
    def quit_script(self) -> None:
        """!
        @brief  Will print a message and ungracefully exit with 1
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        self._log_user_method("QUIT", "Exiting script.", ts)

        # Ensure cleanup happens before exit
        self.cleanup()
        exit(1)

    # --------------------------------------------------------------------------
    def enable_report(self, enable=True):
        """!
        @brief      Used if user wants to enable report
        """
        self._report_enabled = enable

    # --------------------------------------------------------------------------
    def _save_report(self) -> bool:
        """!
        @brief

        @retval     True:
        @retval     False:
        """
        log_path = self.report.get_log_path()
        log_name = self.report.get_log_name()
        report_location = log_path + "/" + log_name

        self._builder_report_header()
        success = self.report.save_report()
        if not success:
            self.error(f"Couldn't save report to '{report_location}'.")
            return False

        self.info(f"Report has been saved to '{report_location}'.")
        return True

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
    def hide_logs_calling_file(self, hide_calling_file=True) -> None:
        """!
        @brief  Will show or hide the file that called logger method,
                printed out based on this state
        """
        self.mb.set_hide_calling_file(hide_calling_file)

    # --------------------------------------------------------------------------
    def set_log_name(self, log_name: str) -> bool:
        """!
        @brief      Allows the user to change what the log is called

        @param      desired log name

        @retval     True: if the name changes was successful
        @retval     False: otherwise
        """
        success = self.report.set_log_name(log_name)
        if not success:
            self.warning(f"Unable to set log name to '{log_name}'. Remaining '{self.report.get_log_name()}'.")
            return True
        return False

    # --------------------------------------------------------------------------
    def set_log_path(self, log_path: str) -> bool:
        """!
        @brief      Allows the user to change where the log is saved

        @param      desired log location

        @retval     True: if the path changes was successful
        @retval     False: otherwise
        """
        success = self.report.set_log_path(log_path)
        if not success:
            self.warning(f"Unable to set log path to '{log_path}'. Remaining '{self.report.get_log_path()}'.")
            return True
        return False

    # --------------------------------------------------------------------------
    def _get_caller_context(self) -> Tuple[str, str, str]:
        """!
        @brief      Extract the calling class and method name

        @returns    Tuple:  file_path(str):   Path to the file that called the log
                            class_name(str):  Name of the class calling the log
                            method_name(str): Name of the method calling the log
        """
        frame = inspect.currentframe()
        logger_class = self.__class__

        file_path = None
        class_name = None
        method_name = None

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
            file_path = os.path.abspath(frame.f_globals['__file__'])

            return file_path, class_name, method_name

        # Print a warning
        if not file_path:
            print("WARNING. File path name found from logger.")
            file_path = "UNKOWN"

        if not class_name:
            print("WARNING. Class name found from logger.")
            class_name = "UNKOWN"

        if not method_name:
            print("WARNING. Method name found from logger.")
            method_name = "UNKOWN"

        return file_path, class_name, method_name

    # --------------------------------------------------------------------------
    def _log_user_method(self, message_type: str, message_to_user: str, time_stamp: str) -> bool:
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
        file_name, class_name, method_name = self._get_caller_context()

        # Build the string
        formatted_message = self.mb.build_log_string(time_stamp=time_stamp,
                                                     calling_file=file_name,
                                                     class_name=class_name,
                                                     method_name=method_name,
                                                     message_type=message_type,
                                                     message_to_user=message_to_user)

        # Save to a report file
        if self._report_enabled:
            self.report.write_line_to_report(formatted_message)

        # Print to terminal
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

    # --------------------------------------------------------------------------
    def _builder_report_header(self):
        """!
        @brief      Builds the header of the report
        """
        self.report.write_to_header(f"========================================================")
        self.report.write_to_header(f"PROGRAM: {self._program_name}")
        self.report.write_to_header(f"CLASS:   {self.__class__.__name__}")
        self.report.write_to_header(f"DATE:    {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.report.write_to_header(f"========================================================")

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


