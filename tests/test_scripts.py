import subprocess
from pathlib import Path
import importlib.util

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(script_name, *, input_text=None, cwd=None):
    script_path = REPO_ROOT / script_name
    result = subprocess.run(
        ["python3", str(script_path)],
        input=input_text,
        text=True,
        capture_output=True,
        cwd=cwd,
        check=True,
    )
    return result.stdout


def test_my_name_docstring():
    path = REPO_ROOT / "my_name.py"
    spec = importlib.util.spec_from_file_location("my_name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.__doc__ == "Casey Summers"


def test_password_stars_output():
    output = run_script("password_stars.py", input_text="secret\n")
    assert output == "Password: ******"


def test_list_files_lists_contents(tmp_path):
    # setup temp directory with known files/directories
    (tmp_path / "subdir").mkdir()
    (tmp_path / "file_a.txt").write_text("A")
    (tmp_path / "file_b.txt").write_text("B")

    output = run_script("list_files.py", cwd=tmp_path)
    lines = output.strip().splitlines()
    assert lines[0].startswith("The files and folders in ")
    listed = set(lines[1:])
    expected = {
        "(d) \tsubdir",
        "(f) \tfile_a.txt",
        "(f) \tfile_b.txt",
    }
    assert expected.issubset(listed)
