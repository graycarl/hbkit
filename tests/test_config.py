# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import pytest
from hbkit import core, config
from hbkit.lib import ConfigManager


defaults = {
    'sec1': {
        'option1': u'sec1.option1.value',
        'option2': u'sec1.option2.value',
    },
    'sec2': {
        'option1': u'sec2.option1.value',
        'optionx': u'333',
    },
    'sec3': {
        'option1': u'true',
        'option2': u'false',
        'option3': u'123',
        'option4': u'no',
        'option5': u'unknown',
        'option6': u'11.22',
        'optionx': None,
    }
}


inicontent = u"""\
[sec1]
option1 = sec1.option1.value.new
option2 = 222

[sec2]
option1 = sec2.option1.value.new
"""


@pytest.fixture
def confpath(tmpdir):
    path = tmpdir.join('config.ini')
    path.write(inicontent)
    return path


def test_load_file(confpath):
    cm = ConfigManager(confpath.strpath, defaults)
    assert cm.get('sec1.option1') == u'sec1.option1.value.new'
    assert cm.get('sec2.optionx') == defaults['sec2']['optionx']
    cm.set('sec1.option1', u'newvalue')
    assert cm.get('sec1.option1') == u'newvalue'


def test_get_values(confpath):
    cm = ConfigManager(confpath.strpath, defaults)
    assert cm.get('sec3.option5') == u'unknown'
    assert cm.get('sec3.option5', str) == u'unknown'

    assert cm.get('sec3.option3', int) == 123
    with pytest.raises(ValueError):
        cm.get('sec3.option5', int)

    assert cm.get('sec3.option1', bool) is True
    assert cm.get('sec3.option2', bool) is False
    assert cm.get('sec3.option4', bool) is False
    with pytest.raises(ValueError):
        cm.get('sec3.option3', bool)

    assert cm.get('sec3.option6', float) < 12
    assert cm.get('sec3.option6', float) > 11
    with pytest.raises(ValueError):
        cm.get('sec3.option4', float)

    assert cm.get('sec3.optionx') is None

    with pytest.raises(cm.OptionNotFound):
        cm.get('sec3.noexists')
    with pytest.raises(cm.OptionNotFound):
        cm.get('secx.option1')


def test_set_values(confpath):
    cm = ConfigManager(confpath.strpath, defaults)
    # set value
    cm.set('sec3.option2', u'yes')
    assert cm.get('sec3.option2') == u'yes'

    # clear value
    cm.set('sec1.option1', None)
    assert cm.get('sec1.option1') == defaults['sec1']['option1']

    # wrong type
    with pytest.raises(RuntimeError):
        cm.set('sec3.option2', True)

    # wrong key
    with pytest.raises(cm.OptionNotFound):
        cm.set('sec3.noexists', 'newvalue')


def test_list_values(confpath):
    cm = ConfigManager(confpath.strpath, defaults)
    item = next(filter(lambda i: i.key == 'sec1.option1', cm.list()))
    assert item.value == 'sec1.option1.value.new'
    assert item.default == defaults['sec1']['option1']
    item = next(filter(lambda i: i.key == 'sec3.option5', cm.list()))
    assert item.value is None
    assert item.default == 'unknown'


def test_save_to_file(confpath):
    cm = ConfigManager(confpath.strpath, defaults)
    old_content = confpath.read()
    assert '[sec3]' not in old_content
    assert 'option1 = sec1.option1.value.new' in old_content
    cm.set('sec3.option2', u'yes')
    cm.set('sec1.option1', None)
    cm.save_to_file()
    new_content = confpath.read()
    assert '[sec3]' in new_content
    assert 'option2 = yes' in new_content
    assert 'option1 = sec1.option1.value.new' not in new_content
    assert 'option2 = 222' in new_content


def test_save_to_new_file(tmpdir):
    confpath = tmpdir.join('confdir').join('newconf.ini')
    cm = ConfigManager(confpath.strpath, defaults)
    cm.set('sec3.option2', u'yes')
    cm.save_to_file()
    new_content = confpath.read()
    assert '[sec3]' in new_content
    assert 'option2 = yes' in new_content


def test_command_list(confpath, monkeypatch, runner):
    monkeypatch.setattr(core, 'config_defaults', defaults)
    g = core.Global(confpath.strpath)
    result = runner.invoke(config.cli_list, obj=g)
    assert '[sec1.option1]: sec1.option1.value.new' in result.output
    assert '[sec3.option5]: unknown' in result.output
    result = runner.invoke(config.cli_list, ['--local'], obj=g)
    assert '[sec1.option1]: sec1.option1.value.new' in result.output
    assert '[sec3.option5]: unknown' not in result.output
    result = runner.invoke(config.cli_list, ['--default'], obj=g)
    assert '[sec1.option1]: sec1.option1.value' in result.output
    assert '[sec3.option5]: unknown' in result.output


def test_command_set(confpath, monkeypatch, runner):
    monkeypatch.setattr(core, 'config_defaults', defaults)
    g = core.Global(confpath.strpath)
    runner.invoke(config.cli_set, ['sec1.option1', 'set_value_1'], obj=g)
    new_content = confpath.read()
    assert 'option1 = set_value_1' in new_content
    assert 'option1 = sec1.option1.value.new' not in new_content


def test_command_unset(confpath, monkeypatch, runner):
    monkeypatch.setattr(core, 'config_defaults', defaults)
    g = core.Global(confpath.strpath)
    runner.invoke(config.cli_unset, ['sec1.option1'], obj=g)
    new_content = confpath.read()
    assert '[sec1]\noption1' not in new_content
    assert '[sec2]\noption1' in new_content
