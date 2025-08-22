from phootlogger import logger


class Test:
    def __init__(self):
        self.msg = logger.messages(__name__)

    def nominal_testing(self):
        """!
        @brief      This test will show what each output is
        """
        self.msg.error("error message here.")
        self.msg.warning("warning message here.")
        self.msg.system("normal message here.")
        self.msg.quit_script()

def main():
    test = Test()
    test.nominal_testing()

if __name__ == "__main__":
    main()
