# -*- coding: utf-8 -*-
from click.testing import CliRunner

from hbkit import random


def test_random_string():
    runner = CliRunner()
    result = runner.invoke(random.cli_string, ['12'])
    assert len(result.output.strip().split()[-1]) == 12


def test_random_number():
    runner = CliRunner()
    result = runner.invoke(random.cli_number, ['4'])
    assert 0 <= int(result.output.strip().split()[-1]) <= 9999


def test_random_uuid():
    runner = CliRunner()
    result = runner.invoke(random.cli_uuid)
    assert len(result.output.strip().split()[-1]) == 32
    result = runner.invoke(random.cli_uuid, ['--split'])
    assert len(result.output.strip().split()[-1]) == 36
