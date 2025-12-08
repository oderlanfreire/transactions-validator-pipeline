import pytest
import os

from modules.util import find_valid_file, move_file_to_hist, smart_file_stem




def test_find_valid_file(tmp_path):
    (tmp_path / 'test_a20251208093645.csv.gz').write_text("col1\n1\n")
    (tmp_path / 'test_a20251208093720.csv').write_text("a\n")

    res = find_valid_file(str(tmp_path))
    assert res.endswith(('test_a20251208093645.csv.gz', 'test_a20251208093720.csv'))

def test_empty_valid_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        find_valid_file(str(tmp_path))


def test_move_to_hist(tmp_path):
    input_dir = tmp_path/"input"
    hist_dir = tmp_path/"hist"

    input_dir.mkdir()
    hist_dir.mkdir()

    f = input_dir/"teste.csv.gz"
    f.write_text("cola\nzhd\n")

    base_name = "teste"
    ts = "20251208_102600"

    moved_to = move_file_to_hist(base_name, ts, input_dir, hist_dir)

    assert not f.exists()
    assert (hist_dir / f"{ts}_teste.csv.gz").exists()
    assert moved_to == str(hist_dir / f"{ts}_teste.csv.gz")



@pytest.mark.parametrize("filename", [
    "teste29a.csv",
    "teste29b.txt",
    "teste29c.csv.gz",
    "teste29d.txt.gz",
])
def test_find_valid_file_accepts_valid_extensions(tmp_path, filename):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    f = input_dir / filename
    f.write_text("a,b\n1,2\n", encoding="utf-8")

    result = find_valid_file(str(input_dir))

    assert result.endswith(filename)


def test_smart_file_stem_invalid_extension(tmp_path):
    f = tmp_path / "teste.xml"
    f.write_text("a1", encoding="utf-8")

    with pytest.raises(ValueError):
        smart_file_stem(str(f))