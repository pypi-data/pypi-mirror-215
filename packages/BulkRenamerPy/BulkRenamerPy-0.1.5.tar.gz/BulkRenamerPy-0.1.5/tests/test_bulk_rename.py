import os
import tempfile

import pytest
from click.testing import CliRunner

from src.bulk_rename import bulk_rename


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def test_files():
    # Create temporary files for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        filenames = ["file1.txt", "file2.txt", "file3.txt"]
        for filename in filenames:
            path = os.path.join(tmpdir, filename)
            with open(path, "w") as f:
                f.write("Test content")
                f.close()

        yield tmpdir, filenames


def test_bulk_rename(runner, test_files):
    tmpdir, filenames = test_files

    # Run the command
    result = runner.invoke(
        bulk_rename,
        [tmpdir, r"file\d\.txt", "new_", "-p", "3", "-l", "2"],
    )

    # Check the command output
    assert result.exit_code == 0
    assert "Renamed: file1.txt -> new_001.txt" in result.output
    assert "Renamed: file2.txt -> new_002.txt" in result.output
    assert "Renamed: file3.txt -> new_003.txt" not in result.output

    # Check the file renaming
    renamed_files = os.listdir(tmpdir)
    renamed_files.sort()
    expected = ["file3.txt", "new_001.txt", "new_002.txt"]
    assert renamed_files == expected


def test_bulk_rename_dry_run(runner, test_files):
    tmpdir, filenames = test_files

    # Run the command with dry-run flag
    result = runner.invoke(
        bulk_rename,
        [tmpdir, r"file\d\.txt", "new_", "-p", "3", "--dry-run"],
    )

    # Check the command output
    assert result.exit_code == 0
    assert "Will rename: file1.txt -> new_001.txt" in result.output
    assert "Will rename: file2.txt -> new_002.txt" in result.output
    assert "Will rename: file3.txt -> new_003.txt" in result.output
    assert "Renamed: file1.txt" not in result.output
    assert "Renamed: file2.txt" not in result.output
    assert "Renamed: file3.txt" not in result.output

    # Check the file names remain unchanged
    original_files = os.listdir(tmpdir)
    original_files.sort()
    assert original_files == filenames


def test_bulk_rename_invalid_directory(runner):
    result = runner.invoke(
        bulk_rename, ["invalid_directory", r"file\d\.txt", "new_", "-p", "3", "-d"]
    )
    assert result.exit_code != 0
    assert (
        "Invalid value for '[DIRECTORY]': Path 'invalid_directory' does not exist."
        in result.output
    )


if __name__ == "__main__":
    pytest.main()
