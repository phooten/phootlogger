
################################################################################
#
# Filename: report.py
#
# Purpose:
#
################################################################################

# TODO: Big todo here. Need to coagulate all the loggers to report to one report.
# Think this is going to require some sort of linking from the user's perspective.
# Need to find a way to enforce this though

################################################################################
class Report:
    """!
    @brief  Class is responsible for handling / saving the output report
            containing the logger's output
    """
    # --------------------------------------------------------------------------
    def __init__(self):
        self.output_path = ""
        self.output_file_name = ""
        self.report = ""

    # --------------------------------------------------------------------------
    def create_output_file_name(self) -> bool:
        """!
        @brief

        @param

        @retval     True
        @retval     False
        """
        pass

    # --------------------------------------------------------------------------
    def set_output_file_name(self) -> bool:
        """!
        @brief

        @param

        @retval     True
        @retval     False
        """
        pass

    # --------------------------------------------------------------------------
    def set_output_path(self, output_path) -> bool:
        """!
        @brief

        @param

        @retval     True
        @retval     False
        """
        # Verify existence of output path

        self.output_path = output_path
        pass

    # --------------------------------------------------------------------------
    def write_line_to_report(self, line: bool) -> bool:
        """!
        @brief      Writes a line to the final logger output file

        @param      line (str): Line to write to the report

        @retval     True:   if write was successful
        @retval     False:  otherwise
        """
        # TODO: Line length?
        pass

    # --------------------------------------------------------------------------
    def save_report(self) -> bool:
        """!
        @brief      Saves the report to the output file / location

        @param

        @retval     True:   if save was successful
        @retval     False:  otherwise
        """
        pass


