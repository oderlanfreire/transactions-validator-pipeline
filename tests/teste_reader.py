import pytest
from modules.reader import read_file

def test_read_file(tmp_path):
    f=tmp_path/'teste.csv'
    f.write_text("col_test1,col_test2\n1,2\n", encoding='utf-8')

    df = read_file(str(f))

    assert len(df) == 1
    assert list(df.columns) == ["col_test1", "col_test2"]

def test_read_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_file("nao_existe.csv")