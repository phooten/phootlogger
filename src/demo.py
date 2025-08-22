from phootlogger import logger


################################################################################
class Test:
    # --------------------------------------------------------------------------
    def __init__(self):
        self.logger = logger.Logger()

    # --------------------------------------------------------------------------
    def nominal_demo(self):
        """!
        @brief      This test will show what each output is
        """
        self.logger.error("error message here.")
        self.logger.warning("warning message here.")
        self.logger.info("normal message here.")

    # --------------------------------------------------------------------------
    def deprecation_demo(self):
        """!
        @brief      This test will what deprecation warnings look like
        """
        # Initializing a deprecated class
        msg = logger.messages()

        # Nominal methods still work
        msg.error("error message here.")

        # Deprecated method still works but will see a warning
        msg.system("normal message here.")

    # --------------------------------------------------------------------------
    def quit_script_demo(self):
        """!
        @brief      This Demo will show what quitting the script looks like
        """
        self.logger.quit_script()
        print("This message will not show up.")

# --------------------------------------------------------------------------
def main():
    test = Test()

    print("\n==========================================")
    print("Start of Nominal Demo")
    print("==========================================\n")
    test.nominal_demo()

    print("\n==========================================")
    print("Start of Deprecation Demo")
    print("==========================================\n")
    test.deprecation_demo()

    print("\n==========================================")
    print("Start of Quit Script Demo")
    print("==========================================\n")
    test.quit_script_demo()

# --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
