import pytest
from types import GeneratorType
from pathlib import Path
from msg_split import split_message


@pytest.mark.parametrize('file,max_len', [('source.html', 4096), ('source.html', 4396), ('source.html', 512),
                                          ('test1.html', 512), ('test1.html', 256), ('test2.html', 100)])
def test_split_message(file, max_len):
    with Path(file).open() as f:
        source = f.read()
    fragments = split_message(source, max_len)

    assert isinstance(fragments, GeneratorType)
    for fragment in fragments:
        assert len(fragment) <= max_len


@pytest.mark.parametrize('file,max_len', [('test2.html', 10), ('source.html', 50), ('test1.html', 25)])
def test_split_messages_when_cant_split_source(file, max_len):
    with Path(file).open() as f:
        source = f.read()

    fragments = split_message(source, max_len)
    with pytest.raises(ValueError):
        for fragment in fragments:
            assert len(fragment) <= max_len
