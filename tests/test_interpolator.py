"""
    tests.test_substitution
    ~~~~~~~~~~~~~~~~~~~~~~~

    Test substitution functions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest

from cfg_loader.exceptions import UnsetRequiredSubstitution, InvalidSubstitution
from cfg_loader.interpolator import SubstitutionTemplate, Interpolator


@pytest.fixture(scope='module')
def interpolator():
    yield Interpolator(substitution_mapping={'VARIABLE': 'value'})


def _test_substitution_base():
    template = SubstitutionTemplate('${VARIABLE}')

    assert template.substitute({'VARIABLE': 'value'}) == 'value'
    assert template.substitute({'VARIABLE': ''}) == ''
    with pytest.raises(KeyError):
        template.substitute({})

    template = SubstitutionTemplate('$VARIABLE')

    assert template.substitute({'VARIABLE': 'value'}) == 'value'
    assert template.substitute({'VARIABLE': ''}) == ''
    with pytest.raises(KeyError):
        template.substitute({})


def _test_substitution_default_if_empty():
    template = SubstitutionTemplate('${VARIABLE:-default}')

    assert template.substitute({'VARIABLE': 'value'}) == 'value'
    assert template.substitute({'VARIABLE': ''}) == 'default'
    assert template.substitute({}) == 'default'


def _test_substitution_default_if_unset():
    template = SubstitutionTemplate('${VARIABLE-default}')

    assert template.substitute({'VARIABLE': 'value'}) == 'value'
    assert template.substitute({'VARIABLE': ''}) == ''
    assert template.substitute({}) == 'default'


def _test_substitution_error_if_unset():
    template = SubstitutionTemplate('${VARIABLE?test error}')

    assert template.substitute({'VARIABLE': 'value'}) == 'value'
    assert template.substitute({'VARIABLE': ''}) == ''
    with pytest.raises(UnsetRequiredSubstitution, message='err') as e:
        template.substitute({})
    assert str(e.value) == 'test error'


def _test_substitution_error_if_empty():
    template = SubstitutionTemplate('${VARIABLE:?test error}')

    assert template.substitute({'VARIABLE': 'value'}) == 'value'
    with pytest.raises(UnsetRequiredSubstitution) as e:
        template.substitute({'VARIABLE': ''})
    assert str(e.value) == 'test error'

    with pytest.raises(UnsetRequiredSubstitution) as e:
        template.substitute({})
    assert str(e.value) == 'test error'


def _test_substitution_complex():
    template = SubstitutionTemplate('/usr/${VARIABLE-default}/app')
    assert template.substitute({'VARIABLE': 'src'}) == '/usr/src/app'
    assert template.substitute({}) == '/usr/default/app'

    template = SubstitutionTemplate('\"Hello, ${VARIABLE}!\"')
    assert template.substitute({'VARIABLE': 'world'}) == '\"Hello, world!\"'

    template = SubstitutionTemplate('$$VARIABLE')
    assert template.substitute({'VARIABLE': 'world'}) == '$VARIABLE'


def _test_substitution_ignored():
    template = SubstitutionTemplate('no substitution pattern')
    assert template.substitute({}) == 'no substitution pattern'


def _test_substitution_invalid():
    template = SubstitutionTemplate('${VARIABLE')
    with pytest.raises(ValueError):
        template.substitute({'VARIABLE': 'world'})

    template = SubstitutionTemplate('${VARIABLE }')
    with pytest.raises(ValueError):
        template.substitute({'VARIABLE': 'world'})

    template = SubstitutionTemplate('${VARIABLE!}')
    with pytest.raises(ValueError):
        template.substitute({'VARIABLE': 'world'})

    template = SubstitutionTemplate('${}')
    with pytest.raises(ValueError):
        print(template.substitute({'VARIABLE': 'world'}))


def test_substitution():
    _test_substitution_base()
    _test_substitution_default_if_empty()
    _test_substitution_default_if_unset()
    _test_substitution_error_if_unset()
    _test_substitution_error_if_empty()
    _test_substitution_complex()
    _test_substitution_invalid()


def _test_valid_interpolation(interpolator):
    raw_input = {
        'key1': '${VARIABLE}',
        'key2': [
            'element',
            '${EXTRA-default}',
        ],
    }
    assert interpolator.interpolate_recursive(raw_input) == {
        'key1': 'value',
        'key2': [
            'element',
            'default',
        ],
    }


def _test_invalid_interpolation(interpolator):
    input = '${VARIABLE?test error'

    with pytest.raises(InvalidSubstitution):
        interpolator.interpolate(input)


def test_interpolator(interpolator):
    _test_valid_interpolation(interpolator)
    _test_invalid_interpolation(interpolator)
