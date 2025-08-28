################################################################################
#
# Filename: message_builder.py
#
# Purpose:
#
################################################################################

# External imports
import re

################################################################################
class MessageBuilder:
    """!
    @brief  This class is to extract the messiness of building the logs. It
            does all the formatting of the string to be printed out
    """
    # --------------------------------------------------------------------------
    def __init__(self):
        # Flags to decide what to display
        self.hide_source = False
        self.hide_timestamps = False

        # Meant to be extra info, but will look messy
        self.hide_calling_file = True

    # --------------------------------------------------------------------------
    def set_hide_source(self, hide_source=False):
        """!
        @brief  Will show or hide the timestamps printed out based on this state
        """
        self.hide_source = hide_source

    # --------------------------------------------------------------------------
    def set_hide_timestamps(self, hide_timestamps=False):
        """!
        @brief  Will show or hide the source ( class / method names) printed out
                based on this state
        """
        self.hide_timestamps = hide_timestamps

    # --------------------------------------------------------------------------
    def set_hide_calling_file(self, hide_calling_file=True):
        """!
        @brief  Will show or hide the file that owns the log instantiation,
                printed out based on this state
        """
        self.hide_calling_file = hide_calling_file

    # --------------------------------------------------------------------------
    def build_log_string(self,
                         time_stamp: str,
                         calling_file: str,
                         class_name: str,
                         method_name: str,
                         message_type: str,
                         message_to_user ) -> str:
        """!
        @brief  Builds the string to be output to the terminal

        @param  time_stamp (str): time stamp of when the log was called
        @param  calling_file (str): Name of the file that called the logger method
        @param  class_name (str): Name of the class calling the log method
        @param  method_name (str): Name of the method calling the log method
        @param  message_type (str): type of message. i.e. ERROR, INFO, DEBUG, etc.
        @param  message_to_user (str): main message to be shown to the user

        @returns Formatted string to be printed out. Example
        """
        # String will look like:
        #   time_stamp                     calling_file          class_name.method_name       message_type message_to_user
        #   <YYYY-MM-DD HH:MM:SS.ssssss> : <calling_file_file> : <class_name>:<method_name> : <TYPE> : <message>

        # Timestamp: 22 characters
        f_time_stamp = f"{time_stamp:<25}"

        # Message Type: 8 characters
        f_message_type = f"[{message_type}]"
        f_message_type = f"{f_message_type:<9}"

        # Class / Method Name: 40 characters
        f_class_name = class_name
        f_method_name = method_name
        f_source = f"{f_class_name}.{f_method_name}"
        f_source = f"{f_source:<25}"

        # calling_file of the logger
        f_calling_file = f"{calling_file:<12}"

        # Format message
        f_message_to_user = re.sub(r"\n", "\n\t\t", message_to_user)

        # Build final string
        final_string = ""

        # If user wants to show time stamp
        if not self.hide_timestamps:
            final_string += f"{f_time_stamp} : "

        # If user wants to show calling_file of the logger
        if not self.hide_calling_file:
            final_string += f"{f_calling_file} : "

        # If user wants to show source
        if not self.hide_source:
            final_string += f"{f_source} : "

        # Bare minimum logs show error type and message
        final_string += f"{f_message_type} : {f_message_to_user}"

        return final_string
