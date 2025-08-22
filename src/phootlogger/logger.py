################################################################################
#
# Filename: logger.py
#
# Purpose:  Class create a logger and use generally across many python projects
#
################################################################################

# External imports
import datetime;
import inspect
import re

################################################################################
class Logger:
    """
    Description:    This class can be instantiated in a python project and report
                    consistent logs with timestamps, function names, and classes
    """
    # --------------------------------------------------------------------------
    def __init__(self):
        self._max_character_length = 10
        self._message_type = "UNKNOWN"
        self._user_message = "UNKNOWN"

        # Set up default log format
        self.mb = MessageBuilder()
        self.mb.set_hide_source(False)
        self.mb.set_hide_timestamps(False)

        # Setting up flags
        self._debug_on = False
        self._show_time = False

    # --------------------------------------------------------------------------
    def info(self, msg) -> None:
        """
        @brief      Prints out message to the user

        @param      msg(string): Message to be printed out to user
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
        @brief      Prints out message to the user

        @param      msg(string): Message to be printed out to user
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        if not self._print_user_message("WARNING", msg, ts):
            print("Issue with WARNING log.")
            self.quit_script()

    # --------------------------------------------------------------------------
    def error(self, msg) -> None:
        """
        @brief      Prints out message to the user

        @param      msg(string): Message to be printed out to user
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        if not self._print_user_message("ERROR", msg, ts):
            print("Issue with ERROR log.")
            self.quit_script()

    # --------------------------------------------------------------------------
    def debug(self, msg) -> None:
        """!
        @brief      Prints out message to the user

        @param      msg(string): Message to be printed out to user
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        if self._debug_on:
            if not self._print_user_message("DEBUG", msg, ts):
                print("Issue with DEBUG log.")
                self.quit_script()

    # --------------------------------------------------------------------------
    def quit_script(self):
        """!
        @brief
        """
        # Get time stamp as soon as this is called
        ts = self._get_time_stamp()

        print("Exiting script.")
        exit(1)

    # --------------------------------------------------------------------------
    def set_debug_mode(self, debug_mode=True):
        """!
        @brief
        """
        self._debug_on = debug_mode

    # --------------------------------------------------------------------------
    def hide_logs_timestamps(self, hide_timestamps=False):
        self.mb.set_hide_timestamps(hide_timestamps)

    # --------------------------------------------------------------------------
    def hide_logs_source(self, hide_source=False):
        self.mb.set_hide_source(hide_source)

    # --------------------------------------------------------------------------
    def _get_caller_context(self):
        """!
        @brief      Extract the calling class and method name
        """
        # Skip _get_caller_context, _print_user_message, and log message
        frame = inspect.currentframe().f_back.f_back.f_back
        method_name = frame.f_code.co_name
        class_name = None

        # Determine classname
        if 'self' in frame.f_locals:
            class_name = frame.f_locals["self"].__class__.__name__

        # Print a warning
        if not method_name or not class_name:
            print("WARNING. Method name or Class name not found from logger.")

        return class_name, method_name

    # --------------------------------------------------------------------------
    def _print_user_message(self, message_type, message_to_user, time_stamp) -> bool:
        """!
        @brief

        @param      message_type
        @param      message_to_user
        @param      time_stamp

        @retval     True
        @retval     False
        """
        # Get the calling methods
        class_name, method_name = self._get_caller_context()

        # Build the string
        formatted_message = self.mb.build_log_string(time_stamp=time_stamp,
                                                     message_type=message_type,
                                                     class_name=class_name,
                                                     method_name=method_name,
                                                     message_to_user=message_to_user)

        print(formatted_message)
        return True

    # --------------------------------------------------------------------------
    def _get_time_stamp(self) -> str:
        """!
        @brief
        """
        ct = str(datetime.datetime.now())
        return ct


    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!! START OF DEPRECATION WARNING SECTION
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

    # --------------------------------------------------------------------------
    def system(self, msg):
        self._deprecation_warning()
        self.info(msg)

    # --------------------------------------------------------------------------
    def printUserMessage(self, file_name, func_name, msg_type, msg_to_user) -> str:
        self._deprecation_warning()
        #  No longer used: file_name, func_name
        self._print_user_message(self, msg_type, msg_to_user)

    # --------------------------------------------------------------------------
    def getFileNameAndFunction(self):
        self._deprecation_warning(immediate=True)
        # self._get_file_name_and_function()

    # --------------------------------------------------------------------------
    def getMessageType(self):
        self._deprecation_warning(immediate=True)
        # self._get_message_type(self)

    # --------------------------------------------------------------------------
    def setMessageType(self, message_type) -> bool:
        self._deprecation_warning(immediate=True)
        # self._set_message_type(self, message_type)

    # --------------------------------------------------------------------------
    def setUserMessage(self, file_name, func_name, message) -> bool:
        self._deprecation_warning(immediate=True)
        # self._set_user_message(self, file_name, func_name, message)

    # --------------------------------------------------------------------------
    def getUserMessage(self) -> str:
        self._deprecation_warning(immediate=True)
        # self._get_user_message(self)

    # --------------------------------------------------------------------------
    def setFileName(self, name) -> None:
        self._deprecation_warning(immediate=True)
        # self._set_file_name(self, name)

    # --------------------------------------------------------------------------
    def getFileName(self) -> str:
        self._deprecation_warning(immediate=True)
        # self._get_file_name(self)

    # --------------------------------------------------------------------------
    def getTimeStamp(self) -> str:
        self._deprecation_warning()
        self._get_time_stamp(self)


class messages(Logger):
    def __init__(self):
        print("*****************************************************************")
        print("* WARNING:")
        print("* \tThis class has been DEPRECATED. It's name has been changed to \"Logger\".")
        print("* \tThis specific instance will soon no longer work.")
        print("*****************************************************************")
        super().__init__()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! END OF DEPRECATION WARNING SECTION
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

################################################################################
class MessageBuilder:
    """!
    @brief
    """
    # --------------------------------------------------------------------------
    def __init__(self):
        # Flags to decide what to display
        self.hide_source = True
        self.hide_timestamps = True

    # --------------------------------------------------------------------------
    def set_hide_source(self, hide_source=False):
        """!
        @brief
        """
        self.hide_source = hide_source

    # --------------------------------------------------------------------------
    def set_hide_timestamps(self, hide_timestamps=False):
        """!
        @brief
        """
        self.hide_timestamps = hide_timestamps

    # --------------------------------------------------------------------------
    def build_log_string(self, time_stamp, message_type, class_name, method_name, message_to_user) -> str:
        """!
        @brief
        """
        # String will look like:
        #   Time                         What called it               Message Type        Message
        #   <YYYY-MM-DD HH:MM:SS TZ>    : <class_name>:<method_name> : <TYPE>  : <message>

        # 22 characters
        f_time_stamp = f"{time_stamp:<25}"

        # 8 characters exactly
        f_message_type = f"[{message_type}]"
        f_message_type = f"{f_message_type:<9}"

        # 40 characters exactly
        f_class_name = class_name
        f_method_name = method_name
        f_source = f"{f_class_name}.{f_method_name}"
        f_source = f"{f_source:<25}"

        # Format message
        f_message_to_user = re.sub(r"\n", "\n\t\t", message_to_user)

        # Build final string
        final_string = ""

        # If user wants to show time stamp
        if not self.hide_timestamps:
            final_string += f"{f_time_stamp} : "

        # If user wants to show source
        if not self.hide_source:
            final_string += f"{f_source} : "

        # Bareminimum logs show error type and message
        final_string += f"{f_message_type} : {f_message_to_user}"

        return final_string
