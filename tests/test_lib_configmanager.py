# -*- coding: utf-8 -*-
import pytest
from hbkit.lib import ConfigManager


defaults = {
    'sec1': {
        'option1': 'sec1.option1.value',
        'option2': 'sec1.option2.value',
    },
    'sec2': {
        'option1': 'sec2.option1.value',
        'optionx': '333',
    },
    'sec3': {
        'option1': 'true',
        'option2': 'false',
        'option3': '123',
        'option4': 'no',
        'option5': 'unknown',
        'option6': '11.22'
    }
}


inicontent = """\
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
    assert cm.get('sec1.option1') == 'sec1.option1.value.new'
    assert cm.get('sec2.optionx') == defaults['sec2']['optionx']
    cm.set('sec1.option1', 'newvalue')
    assert cm.get('sec1.option1') == 'newvalue'


def test_get_values(confpath):
    cm = ConfigManager(confpath.strpath, defaults)
    assert cm.get('sec3.option5') == 'unknown'
    assert cm.get('sec3.option5', str) == 'unknown'

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

    with pytest.raises(KeyError):
        cm.get('sec3.noexists')
    with pytest.raises(KeyError):
        cm.get('secx.option1')


def test_set_values(confpath):
    cm = ConfigManager(confpath.strpath, defaults)
    # set value
    cm.set('sec3.option2', 'yes')
    assert cm.get('sec3.option2') == 'yes'

    # clear value
    cm.set('sec1.option1', None)
    assert cm.get('sec1.option1') == defaults['sec1']['option1']

    # wrong type
    with pytest.raises(RuntimeError):
        cm.set('sec3.option2', True)


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
    cm.set('sec3.option2', 'yes')
    cm.set('sec1.option1', None)
    cm.save_to_file()
    new_content = confpath.read()
    assert '[sec3]' in new_content
    assert 'option2 = yes' in new_content
    assert 'option1 = sec1.option1.value.new' not in new_content
    assert 'option2 = 222' in new_content
