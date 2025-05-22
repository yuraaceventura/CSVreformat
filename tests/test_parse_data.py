import pytest
import sys
from main import parse_args, parse_data, write_file


@pytest.fixture
def sample_csv(tmp_path):
    csv_data = """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60"""
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(csv_data)
    return str(csv_file)


@pytest.fixture
def sample_data():
    return [
        ["Alice Johnson", "Marketing", "160", "50", 8000],
        ["Bob Smith", "Design", "150", "40", 6000],
        ["Carol Williams", "Design", "170", "60", 10200]
    ]


def test_parse_args_without_report(monkeypatch):
    test_args = ["main.py", "data.csv"]
    monkeypatch.setattr(sys, 'argv', test_args)
    out_file, paths = parse_args()
    assert out_file == "out.txt"
    assert paths == ["data.csv"]


def test_parse_args_with_report(monkeypatch):
    test_args = ["main.py", "data.csv", "--report", "report.txt"]
    monkeypatch.setattr(sys, 'argv', test_args)
    out_file, paths = parse_args()
    assert out_file == "report.txt"
    assert paths == ["data.csv"]


def test_parse_data(sample_csv):
    data = []
    result = parse_data(data, [sample_csv])
    assert len(result) == 3
    assert result[0] == ["Alice Johnson", "Marketing", "160", "50", 8000]
    assert result[1] == ["Bob Smith", "Design", "150", "40", 6000]
    assert result[2] == ["Carol Williams", "Design", "170", "60", 10200]


def test_parse_data_with_different_headers(tmp_path):
    csv_data = """id,name,department,worked_hours,hourly_wage
4,Dave Brown,IT,120,55"""
    csv_file = tmp_path / "alt_employees.csv"
    csv_file.write_text(csv_data)

    data = []
    result = parse_data(data, [str(csv_file)])

    assert len(result) == 1
    assert result[0][0] == "Dave Brown"
    assert result[0][1] == "IT"
    assert result[0][2] == "120"
    assert result[0][3] == "55"
    assert result[0][4] == 6600


def test_write_file(sample_data, tmp_path):
    output_file = tmp_path / "output.txt"
    write_file(sample_data, str(output_file))

    assert output_file.exists()

    with open(output_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 5

        headers = lines[0].strip().split()
        assert headers == ["name", "department", "hours", "wage", "payout"]

        first_data_row = lines[2].strip().split()
        assert first_data_row[:5] == ["Alice", "Johnson", "Marketing", "160", "50"]


def test_write_file_empty_data(tmp_path):
    output_file = tmp_path / "empty_output.txt"
    write_file([], str(output_file))

    assert output_file.exists()

    with open(output_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 2


def test_integration(sample_csv, tmp_path, monkeypatch):
    output_file = tmp_path / "integration_report.txt"
    monkeypatch.setattr(sys, 'argv', ["main.py", sample_csv, "--report", str(output_file)])

    import main
    main.main()

    assert output_file.exists()
    with open(output_file, 'r') as f:
        content = f.read()
        assert "Alice" in content
        assert "Johnson" in content
        assert "Marketing" in content
        assert "160" in content
        assert "50" in content
        assert "8000" in content