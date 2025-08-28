
################################################################################
#
# Filename: report.py
#
# Purpose:
#
################################################################################

# External imports
import datetime
import os

################################################################################
class Report:
    """!
    @brief  Class is responsible for handling / saving the output report
            containing the logger's output
    """
    # --------------------------------------------------------------------------
    def __init__(self, program_name="UNKNOWN"):
        # Sets sets default values
        self.program_name = program_name
        self.log_path = self._get_default_log_path()
        self.log_name = self._get_default_log_name()

        # Variable to save logs to
        self.report = ""
        self.header = ""

    # --------------------------------------------------------------------------
    def get_log_name(self) -> str:
        """!
        @brief      gets the current log name

        @returns    str: current log name
        """
        return self.log_name

    # --------------------------------------------------------------------------
    def get_log_path(self) -> str:
        """!
        @brief      gets the current log path

        @returns    str: current log path
        """
        return self.log_path

    # --------------------------------------------------------------------------
    def _get_default_log_name(self) -> str:
        """!
        @brief      Creates an output filename with format: YYYY-MM-DD-mmssMMMM_<program-name>.txt
                    where the first part is the current date/time and the second part is from self.program_name

        @returns    str:
        """
        print("calling default log name")
        try:
            # Get current date and time
            now = datetime.datetime.now()

            # Format: YYYY-MM-DD-mmssMMMM
            date_part = now.strftime("%Y-%m-%d-%H%M%S%f")[:-3]  # Remove last 3 digits of microseconds

            # Create the full filename
            filename = f"{date_part}_{self.program_name}.txt"
            print(f"filename = {filename}")
            return filename

        except Exception as e:
            # If any error occurs, return False
            print(f"Some exception occurred: '{e}'")
            return None

    # --------------------------------------------------------------------------
    def set_log_name(self, file_name) -> bool:
        """!
        @brief      Overwrites the output file name

        @param      file_name (str): Name of the file to be used for output

        @retval     True
        @retval     False
        """

        self.log_name = file_name
        return True

    # --------------------------------------------------------------------------
    def _get_default_log_path(self) -> str:
        """!
        @brief      Set the default report location to be where

        @returns    str: default log path
        """
        return "/home/parke/logs"
        return "~/logs"

    # --------------------------------------------------------------------------
    def set_log_path(self, log_path) -> bool:
        """!
        @brief      Sets the output path after verifying it exists and has write privileges

        @param      log_path (str): Path where output files will be written

        @retval     True:   if path exists and has write privileges
        @retval     False:  if path doesn't exist or lacks write privileges
        """
        try:
            # Check if the path exists
            if not os.path.exists(log_path):
                return False

            # Check if it's a directory
            if not os.path.isdir(log_path):
                return False

            # Check write privileges by attempting to create a test file
            test_file = os.path.join(log_path, ".test_write_access")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                # Remove the test file
                os.remove(test_file)
            except (OSError, IOError):
                # Cannot write to this directory
                return False

            # All checks passed, set the output path
            self.log_path = log_path
            return True

        except Exception as e:
            # If any error occurs, return False
            return False

    # --------------------------------------------------------------------------
    def write_line_to_report(self, line: bool) -> bool:
        """!
        @brief      Writes a line to the final logger output file

        @param      line (str): Line to write to the report

        @retval     True:   if write was successful
        @retval     False:  otherwise
        """
        # TODO: Line length?
        self.report += line + "\n"
        return True

    def write_to_header(self, line: str) -> bool:
        self.header += line + "\n"
        return True

    # --------------------------------------------------------------------------
    def save_report(self) -> bool:
        """!
        @brief      Saves the report to the output file / location

        @retval     True:   if save was successful
        @retval     False:  otherwise
        """
        try:
            # Verify output path is set
            if not self.log_path:
                print("Log path is not set.")
                return False

            # Verify output filename is set
            if not self.log_name:
                print("Log name is not set.")
                return False

            # Verify output path still exists and is writable
            if not os.path.exists(self.log_path):
                print(f"Log path doesn't exist: '{self.log_path}'")
                return False

            if not os.path.isdir(self.log_path):
                print(f"Log path isn't a directory: '{self.log_path}'")
                return False

            # Construct full file path
            full_file_path = os.path.join(self.log_path, self.log_name)

            # Check if we can write to the target file location
            try:
                # Test write access to the directory
                test_file = os.path.join(self.log_path, ".test_write_access")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)

            except (OSError, IOError):
                print("OS / IO Error.")
                return False

            # Write the report content to file
            with open(full_file_path, 'w', encoding='utf-8') as f:
                report = self.header + "\n" + self.report
                f.write(report)

            # Verify the file was created and has content
            if not os.path.exists(full_file_path):
                print(f"Log output doesn't exist: '{full_file_path}'")
                return False

            # Check file size to ensure content was written
            if os.path.getsize(full_file_path) == 0:
                print(f"Unable to get log size: '{full_file_path}'")
                return False

            return True

        except Exception as e:
            # If any error occurs, return False
            print(f"Unknown exception: '{e}'")
            return False


