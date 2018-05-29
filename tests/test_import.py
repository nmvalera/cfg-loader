"""
    tests.test_import
    ~~~~~~~~~~~~~~~~~

    Test import

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import cfg_loader


def _test_version(module):
    assert hasattr(module, '__version__')


def _test_all(module):
    assert hasattr(module, '__all__')


def test_import():
    _test_version(cfg_loader)
    _test_all(cfg_loader)
