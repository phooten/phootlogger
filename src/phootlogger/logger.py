# Modules

# External imports
import re
import inspect
from pathlib import Path
import datetime;

################################################################################
class messages:
    # --------------------------------------------------------------------------
    def __init__(self, file_name):
        self._max_character_length = 10
        self._message_type = "UNKNOWN"
        self._user_message = "UNKNOWN"
        self._file_name = "UNKNOWN"
        self._set_file_name(file_name)

    # --------------------------------------------------------------------------
    def error(self, msg) -> None:
        """
        @brief      Prints out message to the user

        @param      msg(string): Message to be printed out to user
        """
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        funcname = module.__name__

        if not self._print_user_message( filename, funcname, "ERROR", msg ):
            self.quit_script()

    # --------------------------------------------------------------------------
    def warning(self, msg) -> None:
        """!
        @brief      Prints out message to the user

        @param      msg(string): Message to be printed out to user
        """

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        funcname = module.__name__

        if not self._print_user_message(filename, funcname,"WARNING", msg):
            self.quit_script()

    # --------------------------------------------------------------------------
    def info(self, msg) -> None:
        """
        @brief      Prints out message to the user

        @param      msg(string): Message to be printed out to user
        """

        # Set information values
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        funcname = module.__name__

        # Try to print the messages
        if not self._print_user_message(filename, funcname, "INFO", msg):
            self.quit_script()

        return

    # --------------------------------------------------------------------------
    def quit_script(self):
        """!
        @brief
        """
        print( "Exiting script.")
        exit(1)

    # --------------------------------------------------------------------------
    def _print_user_message(self, file_name, func_name, msg_type, msg_to_user) -> str:
        """!
        @brief

        @param
        @param
        @param

        @retval     True
        @retval     False
        """
        # Formats the message type then sets it
        if not self._set_message_type(msg_type):
            return False

        # replaces all newlines with new lines and a tab
        msg_to_user = re.sub("\n", "\n\t\t", msg_to_user)

        self._set_user_message(file_name, func_name, msg_to_user)

        print(self._get_user_message())

        return True

    # --------------------------------------------------------------------------
    def _get_file_name_and_function(self):
        """!
        @brief
        """
        caller_path = Path(inspect.stack()[1][1])
        print(f'{caller_path.name}: ')

    # --------------------------------------------------------------------------
    def _get_message_type(self):
        return self._message_type

    # --------------------------------------------------------------------------
    def _set_message_type(self, message_type) -> bool:
        """!
        @brief

        @param

        @retval     True
        @retval     False
        """

        # Checks the message length
        length = len(message_type)
        if(length > self._max_character_length):
            print(__name__ + ": ["+ str( length ) + "] is too many character. Max is [" + self._max_character_length + "].")
            return False

        # Sets everything to spaces, with one extra space for a ':' at the end
        formatted_message_type = ""
        for curr in range(self._max_character_length + 1):
            formatted_message_type += " "

        # Formats the message type
        for curr in range(len(message_type)):
            formatted_message_type = formatted_message_type[:curr] +  message_type[curr] + formatted_message_type[curr+1:]

        formatted_message_type = formatted_message_type[:(len(message_type))] + ":" + formatted_message_type[(len(message_type) + 1):]

        self._message_type = formatted_message_type

        return True

    # --------------------------------------------------------------------------
    def _set_user_message(self, file_name, func_name, message) -> bool:
        """!
        @brief

        @param
        @param
        @param

        @retval     True
        @retval     False
        """
        self._user_message = self.getTimeStamp() + ": '" + file_name + "' : '" + func_name + "' : " + self._get_message_type() + message
        return True

    # --------------------------------------------------------------------------
    def _get_user_message(self) -> str:
        return self._user_message

    # --------------------------------------------------------------------------
    def _set_file_name(self, name) -> None:
        self._file_name = name

    # --------------------------------------------------------------------------
    def _get_file_name( self ) -> str:
        return self._file_name

    # --------------------------------------------------------------------------
    def _get_time_stamp( self ) -> str:
        """!
        @brief
        """
        ct = str( datetime.datetime.now() )
        return ct


    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!! DEPRECATION WARNING SECTION
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # --------------------------------------------------------------------------
    def _deprecation_warning(self):
        """!
        @brief      Notify users this method will be deprecated soon.
        """
        print("WARNING. This method will soon be DEPRECATED.")

    # --------------------------------------------------------------------------
    def system(self, msg):
        self._deprecation_warning()
        self.info(msg)

    # --------------------------------------------------------------------------
    def printUserMessage(self, file_name, func_name, msg_type, msg_to_user) -> str:
        self._deprecation_warning()
        self._print_user_message(self, file_name, func_name, msg_type, msg_to_user)

    # --------------------------------------------------------------------------
    def getFileNameAndFunction(self):
        self._deprecation_warning()
        self._get_file_name_and_function()

    # --------------------------------------------------------------------------
    def getMessageType(self):
        self._deprecation_warning()
        self._get_message_type(self)

    # --------------------------------------------------------------------------
    def setMessageType(self, message_type) -> bool:
        self._deprecation_warning()
        self._set_message_type(self, message_type)

    # --------------------------------------------------------------------------
    def setUserMessage(self, file_name, func_name, message) -> bool:
        self._deprecation_warning()
        self._set_user_message(self, file_name, func_name, message)

    # --------------------------------------------------------------------------
    def getUserMessage(self) -> str:
        self._deprecation_warning()
        self._get_user_message(self)

    # --------------------------------------------------------------------------
    def setFileName(self, name) -> None:
        self._deprecation_warning()
        self._set_file_name(self, name)

    # --------------------------------------------------------------------------
    def getFileName( self ) -> str:
        self._deprecation_warning()
        self._get_file_name( self )

    # --------------------------------------------------------------------------
    def getTimeStamp( self ) -> str:
        self._deprecation_warning()
        self._get_time_stamp( self )




