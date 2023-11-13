"""
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# Modules
import sys
import re

# Project Modules
#   NA

# TODO This can be taken out and put in it's own project so it can be used across many things

class messages:

    def __init__( self ):
        self._max_character_length = 10
        self._message_type = ""
        self._user_message = ""

        return

    def error( self, msg, func_name ):
        """
        Description:    Prints out message to the user
        Arguments:      msg     - (string) to be printed out to user
                        func_name - (function) function called that figures out what the 
                                name of the previous funcion is
        Returns:        Void
        """

        if not self.printUserMessage( func_name, "ERROR", msg ):
            self.quit_script()

        return


    def warning( self, msg, func_name ):
        """
        Description:    Prints out message to the user
        Arguments:      msg     - (string) to be printed out to user
                        func_name - (function) function called that figures out what the 
                                name of the previous funcion is
        Returns:        Void
        """

        if not self.printUserMessage( func_name, "WARNING", msg ):
            self.quit_script()

        return


    def system( self, msg, func_name ):
        """
        Description:    Prints out message to the user
        Arguments:      msg     - (string) to be printed out to user
                        func_name - (function) function called that figures out what the 
                                name of the previous funcion is
        Returns:        Void
        """

        if not self.printUserMessage( func_name, "SYSTEM", msg ):
            self.quit_script()

        return


    def quit_script( self ):

        print( "Exiting script.")
        exit(1)


    def printUserMessage( self, func_name, msg_type, msg_to_user ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        # Formats the message type then sets it
        if not self.setMessageType( msg_type ):
            return False

        # replaces all newlines with new lines and a tab
        msg_to_user = re.sub( "\n", "\n\t\t", msg_to_user )

        # Prints final message
        print( func_name + ": " + self.getMessageType() + msg_to_user )

        return True


    def getMessageType( self ):
        return self._message_type

    def setMessageType( self, message_type ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        # Checks the message length
        length = len( message_type )
        if( length > self._max_character_length ):
            print( __name__ + ": ["+ str( length ) + "] is too many character. Max is [" + max_character_length + "]." )
            return False

        # Sets everything to spaces, with one extra space for a ':' at the end
        formatted_message_type = ""
        for curr in range( self._max_character_length + 1 ):
            formatted_message_type += " "

        # Formats the message type
        for curr in range( len( message_type ) ):
            formatted_message_type = formatted_message_type[ :curr ] +  message_type[ curr ] + formatted_message_type[ curr+1: ]

        formatted_message_type = formatted_message_type[ :( len( message_type )) ] + ":" + formatted_message_type[ ( len( message_type ) + 1): ]

        self._message_type = formatted_message_type

        return True


    def setUserMessage( self, message, func_name ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        self._user_message = func_name + ": " + getMessageType() + " " + getMessage()

        return True

    def getUserMessage( self ):
        return self._user_message