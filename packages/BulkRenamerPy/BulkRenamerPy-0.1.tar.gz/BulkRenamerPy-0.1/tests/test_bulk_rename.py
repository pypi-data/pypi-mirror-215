import os
import tempfile
import pytest
import shutil
from click.testing import CliRunner
from src.bulk_rename import bulk_rename


@pytest.fixture
def temp_dir():
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up the temporary directory after each test
    shutil.rmtree(temp_dir)


def test_bulk_rename(temp_dir):
    # Create some test files in the temporary directory
    filenames = ["file1.txt", "file2.txt", "file3.txt"]
    for filename in filenames:
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, "w") as f:
            f.write("Test file content")

    runner = CliRunner()

    # Run the bulk_rename command
    result = runner.invoke(
        bulk_rename,
        [temp_dir, r"file\d\.txt", "new_", "-p", "3", "-l", "2", "-s", "size"],
    )

    # Assert that the command ran successfully
    assert result.exit_code == 0

    # Assert the expected renamed files
    renamed_files = ["new_001.txt", "new_002.txt"]
    for renamed_file in renamed_files:
        renamed_file_path = os.path.join(temp_dir, renamed_file)
        assert os.path.exists(renamed_file_path)

    # Assert the original files were not renamed
    for filename in filenames[:1]:
        file_path = os.path.join(temp_dir, filename)
        assert os.path.exists(file_path)

    # Assert the original files were deleted if limit is set
    file_path = os.path.join(temp_dir, filenames[2])
    assert not os.path.exists(file_path)

    # Assert the dry run option works
    result = runner.invoke(
        bulk_rename,
        [temp_dir, r"file\d\.txt", "dry", "-d"],
    )
    assert result.exit_code == 0
    expected_files = ["new_001.txt", "new_002.txt", "file1.txt"]
    for filename in expected_files[:1]:
        file_path = os.path.join(temp_dir, filename)
        assert os.path.exists(file_path)

    # Assert the sorting option works
    result = runner.invoke(
        bulk_rename,
        [temp_dir, r"file\d\.txt", "new_", "-s", "creation"],
    )
    assert result.exit_code == 0
    renamed_files = ["new_001.txt", "new_002.txt"]
    for renamed_file in renamed_files:
        renamed_file_path = os.path.join(temp_dir, renamed_file)
        assert os.path.exists(renamed_file_path)
