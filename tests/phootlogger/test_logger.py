import pytest
from unittest.mock import patch, ANY

from phootlogger.logger import Logger


@pytest.fixture
def logger_fixture():
    logger = Logger()
    return logger


class TestLogger:
    def test_info_successful_log(self, logger_fixture):
        """!
        @brief
        """
        with patch.object(logger_fixture, '_print_user_message', return_value=True) as mock_print:
            expected_message = "Info Test message"
            logger_fixture.info(expected_message)
            mock_print.assert_called_once_with("INFO", expected_message, ANY)

    def test_info_failed_log_triggers_quit(self, logger_fixture):
        """!
        @brief
        """
        with patch.object(logger_fixture, '_print_user_message', return_value=False), \
             patch.object(logger_fixture, 'quit_script') as mock_quit, \
             patch('builtins.print') as mock_print:
            logger_fixture.info("Info Test failure")
            mock_print.assert_called_with("Issue with INFO log.")
            mock_quit.assert_called_once()

    def test_warning_successful_log(self, logger_fixture):
        """!
        @brief
        """
        with patch.object(logger_fixture, '_print_user_message', return_value=True) as mock_print:
            expected_message = "Warning Test message"
            logger_fixture.warning(expected_message)
            mock_print.assert_called_once_with("WARNING", expected_message, ANY)

    def test_warning_failed_log_triggers_quit(self, logger_fixture):
        """!
        @brief
        """
        with patch.object(logger_fixture, '_print_user_message', return_value=False), \
             patch.object(logger_fixture, 'quit_script') as mock_quit, \
             patch('builtins.print') as mock_print:
            logger_fixture.warning("Warning Test failure")
            mock_print.assert_called_with("Issue with WARNING log.")
            mock_quit.assert_called_once()

    def test_error_successful_log(self, logger_fixture):
        """!
        @brief
        """
        with patch.object(logger_fixture, '_print_user_message', return_value=True) as mock_print:
            expected_message = "Error Test message"
            logger_fixture.error(expected_message)
            mock_print.assert_called_once_with("ERROR", expected_message, ANY)

    def test_error_failed_log_triggers_quit(self, logger_fixture):
        """!
        @brief
        """
        with patch.object(logger_fixture, '_print_user_message', return_value=False), \
             patch.object(logger_fixture, 'quit_script') as mock_quit, \
             patch('builtins.print') as mock_print:
            logger_fixture.error("Error Test failure")
            mock_print.assert_called_with("Issue with ERROR log.")
            mock_quit.assert_called_once()

    def test_debug_successful_log(self, logger_fixture):
        """!
        @brief
        """
        original_state = logger_fixture._debug_mode
        logger_fixture.set_debug_mode(True)

        with patch.object(logger_fixture, '_print_user_message', return_value=True) as mock_print:
            expected_message = "Debug Test message"
            logger_fixture.debug(expected_message)
            mock_print.assert_called_once_with("DEBUG", expected_message, ANY)

        logger_fixture.set_debug_mode(original_state)

    def test_debug_successful_log_hidden(self, logger_fixture):
        """!
        @brief
        """
        original_state = logger_fixture._debug_mode
        logger_fixture.set_debug_mode(False)

        with patch.object(logger_fixture, '_print_user_message', return_value=True) as mock_print:
            logger_fixture.debug("Debug Test message")
            mock_print.assert_not_called()

        logger_fixture.set_debug_mode(original_state)

    def test_debug_failed_log_triggers_quit(self, logger_fixture):
        """!
        @brief
        """
        original_state = logger_fixture._debug_mode
        logger_fixture.set_debug_mode(True)

        with patch.object(logger_fixture, '_print_user_message', return_value=False), \
             patch.object(logger_fixture, 'quit_script') as mock_quit, \
             patch('builtins.print') as mock_print:
            logger_fixture.debug("Debug Test failure")
            mock_print.assert_called_with("Issue with DEBUG log.")
            mock_quit.assert_called_once()

        logger_fixture.set_debug_mode(original_state)



