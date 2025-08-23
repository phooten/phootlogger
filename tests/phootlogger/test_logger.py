from unittest.mock import patch, MagicMock, ANY
import datetime
import inspect
import pytest
import re

# Internal Import
from phootlogger.logger import MessageBuilder  # Adjust import as needed
from phootlogger.logger import Logger

@pytest.fixture
def logger_fixture():
    return Logger()

@pytest.fixture
def message_builder_fixture():
    return MessageBuilder()

class DummyCaller:
    def __init__(self):
        self.logger = Logger()

    def trigger_context(self):
        return self.logger._get_caller_context()

# Off-nominal: Called from static method (no self)
class StaticCaller:
    logger = Logger()

    @staticmethod
    def static_trigger():
        return StaticCaller.logger._get_caller_context()

# Off-nominal: Called from global function
def global_trigger(logger):
    return logger._get_caller_context()

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


    def test_quit_script_calls_exit_and_prints(self, logger_fixture):
        # Mock timestamp and exit
        logger_fixture._get_time_stamp = lambda: "2025-08-22 18:45:00"

        with patch("builtins.print") as mock_print, patch("builtins.exit") as mock_exit:
            logger_fixture.quit_script()

        mock_print.assert_called_once_with("Exiting script.")
        mock_exit.assert_called_once_with(1)

    def test_quit_script_uses_timestamp(self, logger_fixture):
        with patch.object(logger_fixture, "_get_time_stamp", return_value="mocked-ts") as mock_ts, \
             patch("builtins.exit"), \
             patch("builtins.print"):
            logger_fixture.quit_script()

        mock_ts.assert_called_once()


    def test_nominal_class_and_method_detected(self):
        """!
        @brief
        """
        caller = DummyCaller()
        class_name, method_name = caller.trigger_context()
        assert class_name == "DummyCaller"
        assert method_name == "trigger_context"

    # Nominal: Called directly from test function
    def test_nominal_direct_call(self, logger_fixture):
        """!
        @brief
        """
        class_name, method_name = logger_fixture._get_caller_context()
        assert class_name == "TestLogger"
        assert method_name == "test_nominal_direct_call"


    def test_off_nominal_static_method(self):
        """!
        @brief
        """
        class_name, method_name = StaticCaller.static_trigger()
        assert class_name is None
        assert method_name == "static_trigger"

    def test_off_nominal_global_function(self, logger_fixture):
        """!
        @brief
        """
        class_name, method_name = global_trigger(logger_fixture)
        assert class_name is None
        assert method_name == "global_trigger"

    # Off-nominal: Called from within logger itself
    def test_off_nominal_internal_logger_call(self, logger_fixture):
        """!
        @brief
        """
        # Simulate internal call chain
        class_name, method_name = logger_fixture._get_caller_context()
        # Should skip internal frames and return test function
        assert method_name.startswith("test_")

    # Defensive: Max depth exceeded
    def test_off_nominal_max_depth_safeguard(self):
        """!
        @brief
        """
        class SafeLogger(Logger):
            def _get_caller_context(self, max_depth=1):
                frame = inspect.currentframe()
                depth = 0
                while frame and depth < max_depth:
                    frame = frame.f_back
                    depth += 1
                return None, None

        logger = SafeLogger()
        class_name, method_name = logger._get_caller_context()
        assert class_name is None
        assert method_name is None


    def test_print_user_message_nominal(self, logger_fixture):
        """!
        @brief
        """
        logger_fixture.owner_filepath = "/path/to/owner"

        # Mock dependencies
        logger_fixture._get_caller_context = MagicMock(return_value=("TestClass", "test_method"))
        logger_fixture.mb = MagicMock()
        logger_fixture.mb.build_log_string = MagicMock(return_value="Formatted log message")

        with patch("builtins.print") as mock_print:
            result = logger_fixture._print_user_message(
                message_type="INFO",
                message_to_user="Hello, world!",
                time_stamp="2025-08-22 18:30:00"
            )

        # Assertions
        logger_fixture._get_caller_context.assert_called_once()
        logger_fixture.mb.build_log_string.assert_called_once_with(
            time_stamp="2025-08-22 18:30:00",
            message_type="INFO",
            class_name="TestClass",
            method_name="test_method",
            message_to_user="Hello, world!",
            owner="/path/to/owner"
        )
        mock_print.assert_called_once_with("Formatted log message")
        assert result is True

    def test_print_user_message_missing_context(self, logger_fixture):
        """!
        @brief
        """
        logger_fixture.owner_filepath = "/path/to/owner"

        logger_fixture._get_caller_context = MagicMock(return_value=(None, None))
        logger_fixture.mb = MagicMock()
        logger_fixture.mb.build_log_string = MagicMock(return_value="Fallback log message")

        with patch("builtins.print") as mock_print:
            result = logger_fixture._print_user_message(
                message_type="WARNING",
                message_to_user="Something went wrong",
                time_stamp="2025-08-22 18:35:00"
            )

        mock_print.assert_called_once_with("Fallback log message")
        assert result is True

    @pytest.mark.parametrize("msg_type", ["INFO", "DEBUG", "ERROR", "WARNING"])
    def test_print_user_message_varied_types(self, logger_fixture, msg_type):
        """!
        @brief
        """
        logger_fixture.owner_filepath = "owner.txt"
        logger_fixture._get_caller_context = MagicMock(return_value=("Caller", "caller_method"))
        logger_fixture.mb = MagicMock()
        logger_fixture.mb.build_log_string = MagicMock(return_value=f"{msg_type} log")

        with patch("builtins.print") as mock_print:
            result = logger_fixture._print_user_message(
                message_type=msg_type,
                message_to_user="Test message",
                time_stamp="2025-08-22 18:40:00"
            )

        mock_print.assert_called_once_with(f"{msg_type} log")
        assert result is True


    def test_get_time_stamp_returns_expected_format(self, logger_fixture):
        """!
        @brief
        """
        fixed_time = datetime.datetime(2025, 8, 22, 18, 41, 0)
        expected = str(fixed_time)

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = fixed_time
            mock_datetime.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)

            result = logger_fixture._get_time_stamp()

        assert result == expected

    def test_get_time_stamp_is_string(self, logger_fixture):
        """!
        @brief
        """
        result = logger_fixture._get_time_stamp()
        assert isinstance(result, str)

    def test_get_time_stamp_changes_over_time(self, logger_fixture):
        """!
        @brief
        """
        first = logger_fixture._get_time_stamp()
        second = logger_fixture._get_time_stamp()
        assert first <= second  # Should be equal or later


class TestMessageBuilder:

    def test_default_formatting(self, message_builder_fixture):
        result = message_builder_fixture.build_log_string(
            time_stamp="2025-08-22 18:45:00",
            message_type="INFO",
            class_name="TestClass",
            method_name="test_method",
            message_to_user="Hello, world!",
            owner="owner.py"
        )

        assert "[INFO]" in result
        assert "TestClass.test_method" in result
        assert "owner.py" not in result  # hidden by default
        assert "2025-08-22 18:45:00" in result
        assert "Hello, world!" in result

    def test_hide_source_flag(self, message_builder_fixture):
        message_builder_fixture.set_hide_source(True)

        result = message_builder_fixture.build_log_string(
            time_stamp="2025-08-22 18:45:00",
            message_type="DEBUG",
            class_name="HiddenClass",
            method_name="hidden_method",
            message_to_user="No source shown",
            owner="owner.py"
        )

        assert "HiddenClass.hidden_method" not in result
        assert "[DEBUG]" in result
        assert "No source shown" in result

    def test_hide_timestamps_flag(self, message_builder_fixture):
        message_builder_fixture.set_hide_timestamps(True)

        result = message_builder_fixture.build_log_string(
            time_stamp="2025-08-22 18:45:00",
            message_type="ERROR",
            class_name="TimeClass",
            method_name="time_method",
            message_to_user="No timestamp",
            owner="owner.py"
        )

        assert "2025-08-22" not in result
        assert "[ERROR]" in result

    def test_hide_owner_flag(self, message_builder_fixture):
        message_builder_fixture.set_hide_owner(False)

        result = message_builder_fixture.build_log_string(
            time_stamp="2025-08-22 18:45:00",
            message_type="WARNING",
            class_name="OwnerClass",
            method_name="owner_method",
            message_to_user="Owner visible",
            owner="owner.py"
        )

        assert "owner.py" in result
        assert "[WARNING]" in result

    def test_multiline_message_formatting(self, message_builder_fixture):
        multiline_message = "Line one\nLine two\nLine three"
        result = message_builder_fixture.build_log_string(
            time_stamp="2025-08-22 18:45:00",
            message_type="INFO",
            class_name="MultiClass",
            method_name="multi_method",
            message_to_user=multiline_message,
            owner="owner.py"
        )

        # Check that newlines are indented
        assert "\n\t\tLine two" in result
        assert "\n\t\tLine three" in result
