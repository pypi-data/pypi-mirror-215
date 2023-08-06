import pytest

from src.escp import Commands_9_Pin, CharacterTable


@pytest.fixture
def commands():
    return Commands_9_Pin()


@pytest.mark.parametrize('numerator,denominator,codes', [(1, 6, b'\x1b2'), (1, 8, b'\x1b0'), (45, 216, b'\x1b3\x2d')])
def test_line_spacing(commands, numerator, denominator, codes):
    assert commands.line_spacing(numerator, denominator).buffer == codes


@pytest.mark.parametrize('ct,expected_buffer', [(0, b'\x1bt\x00'), (1, b'\x1bt\x01')])
def test_select_character_table(commands, ct, expected_buffer):
    assert commands.select_character_table(ct).buffer == expected_buffer


def test_select_character_table_invalid(commands):
    with pytest.raises(ValueError):
        commands.select_character_table(2)


@pytest.mark.parametrize(
    'table,character_table,expected_buffer',
    [
        (0, CharacterTable.ITALIC, b'\x1b\x28\x74\x03\x00\x00\x00\x00'),
        (0, CharacterTable.PC437_US, b'\x1b\x28\x74\x03\x00\x00\x01\x00'),
        (1, CharacterTable.PC437_US, b'\x1b\x28\x74\x03\x00\x01\x01\x00'),
        (1, CharacterTable.PC_AR864, b'\x1b\x28\x74\x03\x00\x01\x0d\x20'),
    ]
)
def test_assign_character_table(commands, table, character_table, expected_buffer):
    assert commands.assign_character_table(table, character_table).buffer == expected_buffer
