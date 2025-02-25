# standard libraries
from pathlib import Path

import pytest

from innofw.constants import DefaultS3User
from innofw.zoo import download_model

# third-party libraries
# local modules


@pytest.mark.parametrize(
    ["file_url", "credentials"],
    [
        [
            "https://api.blackhole.ai.innopolis.university/pretrained/testing/best.pkl",
            DefaultS3User,
        ]
    ],
)
def test_download_model(file_url, tmp_path, credentials):
    downloaded_file: Path = download_model(
        file_url,
        tmp_path,
        credentials.ACCESS_KEY.get_secret_value(),
        credentials.SECRET_KEY.get_secret_value(),
    )

    assert downloaded_file.exists()
    assert downloaded_file.parent == tmp_path

    downloaded_file.unlink()

    # Test case 1: Try to download a file that doesn't exist and check if it raises an exception.
    with pytest.raises(Exception):
        download_model(
            "https://api.blackhole.ai.innopolis.university/pretrained/testing/invalid_file.pkl",
            tmp_path,
            credentials.ACCESS_KEY.get_secret_value(),
            credentials.SECRET_KEY.get_secret_value(),
        )

    # Test case 2: Try to download a file in other folder and check if the file is saved in other folder.
    dst_path = tmp_path / "other_folder"
    downloaded_file: Path = download_model(
        file_url,
        dst_path,
        credentials.ACCESS_KEY.get_secret_value(),
        credentials.SECRET_KEY.get_secret_value(),
    )
    assert downloaded_file.exists()
    assert dst_path.exists()
