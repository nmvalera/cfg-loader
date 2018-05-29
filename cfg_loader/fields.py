"""
    cfg_loader.fields
    ~~~~~~~~~~~~~~~~~

    Implement marshmallow fields to validate against specific input data

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import os

from marshmallow import validate, fields


class PathValidator(validate.Validator):
    """Validate a path.

    :param error: Error message to raise in case of a validation error. Can be
        interpolated with `{input}`.
    :type error: str
    """

    default_message = 'Path "{input}" does not exist'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(input=value)

    def __call__(self, value):
        message = self._format_error(value)

        if not os.path.exists(value):
            raise validate.ValidationError(message)

        return value


class Path(fields.String):
    """A validated path field. Validation occurs during both serialization and
    deserialization.

    :param args: The same positional arguments that :class:`~marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that :class:`~marshmallow.fields.String` receives.
    """

    default_error_messages = {'invalid_path': 'Path "{input}" does not exist'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        self.validators.append(PathValidator(error=self.error_messages['invalid_path']))


class UnwrapNested(fields.Nested):
    """Nested fields class that will unwrapped at deserialization

    Useful when used with UnwrapSchema

    :param prefix: Optional prefix to add to every key when unwrapping a field
    :type prefix: str
    """

    def __init__(self, *args, prefix='', **kwargs):
        self.prefix = prefix
        super().__init__(*args, **kwargs)
