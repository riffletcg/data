from riffletcg_data import __version__
from riffletcg_data.main import main


def test_version():
    assert __version__


def test_main_succeeds(capsys):
    assert main() == 0
    assert "riffletcg-data" in capsys.readouterr().out
