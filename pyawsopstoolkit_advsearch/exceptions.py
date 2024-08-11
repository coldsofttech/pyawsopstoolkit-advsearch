from typing import Optional, Union

from pyawsopstoolkit_advsearch.__validations__ import _validate_type


class AdvanceSearchError(AttributeError):
    """
    Custom exception class for AWS Ops Toolkit. This exception is typically raised during advance search failures.
    """

    def __init__(
            self,
            message: str,
            exception: Optional[Exception] = None
    ) -> None:
        """
        Constructor for the AdvanceSearchError class.

        :param message: The error message.
        :type message: str
        :param exception: The exception that occurred, if any.
        :type exception: Exception
        """
        _validate_type(message, str, 'message should be a string.')
        _validate_type(exception, Union[Exception, None], 'exception should be of Exception type.')

        self._exception = exception
        self._message = f'ERROR: {message}.{f" {exception}." if exception else ""}'
        super().__init__(self._message)

    @property
    def exception(self) -> Optional[Exception]:
        """
        Getter for exception attribute.

        :return: The exception that occurred, if any.
        :rtype: Exception
        """
        return self._exception

    @property
    def message(self) -> str:
        """
        Getter for message attribute.

        :return: The error message.
        :rtype: str
        """
        return self._message


class SearchAttributeError(AttributeError):
    """
    Custom exception class for AWS Ops Toolkit. This exception is typically raised when either invalid attributes are
    provided or key attributes are missing.
    """

    def __init__(
            self,
            message: str,
            exception: Optional[Exception] = None
    ) -> None:
        """
        Constructor for the SearchAttributeError class.

        :param message: The error message.
        :type message: str
        :param exception: The exception that occurred, if any.
        :type exception: Exception
        """
        _validate_type(message, str, 'message should be a string.')
        _validate_type(exception, Union[Exception, None], 'exception should be of Exception type.')

        self._exception = exception
        self._message = f'ERROR: {message}.{f" {exception}." if exception else ""}'
        super().__init__(self._message)

    @property
    def exception(self) -> Optional[Exception]:
        """
        Getter for exception attribute.

        :return: The exception that occurred, if any.
        :rtype: Exception
        """
        return self._exception

    @property
    def message(self) -> str:
        """
        Getter for message attribute.

        :return: The error message.
        :rtype: str
        """
        return self._message
