"""
    cfg_loader.interpolation
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Implement functions to substitute environment variable input data

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import re
import string

from .exceptions import UnsetRequiredSubstitution, InvalidSubstitution

# Brace formatted syntax separators (c.f. https://docs.docker.com/compose/compose-file/#variable-substitution)
SEPARATOR_DEFAULT_IF_EMPTY = ':-'
SEPARATOR_DEFAULT_IF_UNSET = '-'
SEPARATOR_ERROR_IF_EMPTY = ':?'
SEPARATOR_ERROR_IF_UNSET = '?'


class SubstitutionTemplate(string.Template):
    """Class used to substitute environment variables in a string

    It implements specification from docker-compose environ variable substitution
    (c.f. https://docs.docker.com/compose/compose-file/#variable-substitution)

    Examples with basic substitution

    >>> template = SubstitutionTemplate('${VARIABLE}')
    >>> template.substitute({'VARIABLE': 'value'})
    'value'
    >>> template.substitute({'VARIABLE': ''})
    ''
    >>> template.substitute({})
    Traceback (most recent call last):
    ...
    KeyError: 'VARIABLE'

    Examples with substitution if variable is empty or unset (separator: ":-")

    >>> template = SubstitutionTemplate('${VARIABLE:-default}')
    >>> template.substitute({'VARIABLE': 'value'})
    'value'
    >>> template.substitute({'VARIABLE': ''})
    'default'
    >>> template.substitute({})
    'default'

    Examples with substitution if variable is empty (separator: "-"):

    >>> template = SubstitutionTemplate('${VARIABLE-default}')
    >>> template.substitute({'VARIABLE': 'value'})
    'value'
    >>> template.substitute({'VARIABLE': ''})
    ''
    >>> template.substitute({})
    'default'

    Examples with error raised if variable is unset (separator: "?")

    >>> template = SubstitutionTemplate('${VARIABLE?err}')
    >>> template.substitute({'VARIABLE': 'value'})
    'value'
    >>> template.substitute({'VARIABLE': ''})
    ''
    >>> template.substitute({})
    Traceback (most recent call last):
    ...
    cfg_loader.exceptions.UnsetRequiredSubstitution: err

    Examples with error raised if variable is empty or  unset (separator: ":?")

    >>> template = SubstitutionTemplate('${VARIABLE:?err}')
    >>> template.substitute({'VARIABLE': 'value'})
    'value'
    >>> template.substitute({'VARIABLE': ''})
    Traceback (most recent call last):
    ...
    cfg_loader.exceptions.UnsetRequiredSubstitution: err
    >>> template.substitute({})
    Traceback (most recent call last):
    ...
    cfg_loader.exceptions.UnsetRequiredSubstitution: err
    """

    pattern = r"""
        %(delim)s(?:
            (?P<escaped>%(delim)s) |
            (?P<named>%(id)s)      |
            {(?P<braced>%(bid)s)}  |
            (?P<invalid>)
        )
        """ % {
        'delim': re.escape('$'),
        'id': r'[_a-z][_a-z0-9]*',
        'bid': r'[_a-z][_a-z0-9]*(?:(?P<sep>:?[-?])[^}]*)?',
    }

    def substitute(self, mapping):
        """Substitute values indexed by mapping into `template`

        :param mapping: Mapping containing values to substitute
        :type mapping: dict
        """

        def convert(mo):
            named, braced = mo.group('named') or mo.group('braced'), mo.group('braced')
            if braced is not None:
                sep = mo.group('sep')
                if sep:
                    return process_braced_group(braced, sep, mapping)

            if named is not None:
                val = mapping[named]
                return '%s' % (val,)

            if mo.group('escaped') is not None:  # pragma: no branch
                return self.delimiter

            if mo.group('invalid') is not None:  # pragma: no branch
                raise ValueError('Invalid placeholder: {}'.format(self.template))

        return self.pattern.sub(convert, self.template)


def process_braced_group(braced, sep, mapping):
    """Parse a braced formatted syntax and returns substituted value or raise error

    It implements specification from docker-compose environ variable substitution
    (c.f. https://docs.docker.com/compose/compose-file/#variable-substitution)

    :param braced: Braced formatted syntax to substitute
    :type braced: str
    :param sep: Separator in the braced syntax
    :type sep: str
    :param mapping: Mapping with values to substitute
    :type mapping: dict
    """

    if sep == SEPARATOR_DEFAULT_IF_EMPTY:
        var, _, default = braced.partition(SEPARATOR_DEFAULT_IF_EMPTY)
        return mapping.get(var) or default

    elif sep == SEPARATOR_DEFAULT_IF_UNSET:
        var, _, default = braced.partition(SEPARATOR_DEFAULT_IF_UNSET)
        return mapping.get(var, default)

    elif sep == SEPARATOR_ERROR_IF_EMPTY:
        var, _, err = braced.partition(SEPARATOR_ERROR_IF_EMPTY)
        rv = mapping.get(var)
        if not rv:
            raise UnsetRequiredSubstitution(err)
        return rv

    elif sep == SEPARATOR_ERROR_IF_UNSET:  # pragma: no branch
        var, _, err = braced.partition(SEPARATOR_ERROR_IF_UNSET)
        if var in mapping:
            return mapping.get(var)
        raise UnsetRequiredSubstitution(err)


class Interpolator:
    """Class used to substitute environment variables in complex object

    :param substitution_mapping: Mapping with values to substitute
    :type substitution_mapping: dict

    Example

    >>> interpolator = Interpolator(substitution_mapping={'VARIABLE': 'value'})

    >>> interpolator.interpolate('${VARIABLE} in complex string')
    'value in complex string'

    >>> result = interpolator.interpolate_recursive({'key1': '${VARIABLE}', 'key2': ['element', '${EXTRA-default}']})
    >>> result == {'key1': 'value', 'key2': ['element', 'default']}
    True
    """

    def __init__(self, substitution_mapping=None, substitution_template=SubstitutionTemplate):
        self._substitution_template = substitution_template
        self._substitution_mapping = substitution_mapping or {}

    def interpolate(self, string):
        """Substitute environment variable in a string"""
        try:
            return self._substitution_template(string).substitute(self._substitution_mapping)
        except ValueError as e:
            raise InvalidSubstitution(e)

    def interpolate_recursive(self, obj):
        """Substitute environment variable in an object"""

        if isinstance(obj, str):
            return self.interpolate(obj)

        elif isinstance(obj, dict):
            return {key: self.interpolate_recursive(value) for key, value in obj.items()}

        elif isinstance(obj, list):
            return [self.interpolate_recursive(element) for element in obj]

        return obj
