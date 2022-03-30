"""
@description: This module tests Encoder class
responsible for encoding/decoding data in base64
from tarfile
@author: abdullahrkw
"""
import io
import os
import pytest

from publisher.utilities.encoder import Encoder


@pytest.fixture
def encoder_obj():
    encoder = Encoder()
    return encoder


def test_if_b64_encoding_working(encoder_obj):
    string_val = "abcd"
    binary_stream = string_val.encode('utf-8')
    expected_val = "YWJjZA=="
    actual_val = encoder_obj.encode_b64(binary_stream).decode('utf-8')
    assert actual_val == expected_val

def test_if_b64_decoding_working(encoder_obj):
    encoded_str = "YWJjZA==".encode('utf-8')
    expected_val = "abcd"
    actual_val = encoder_obj.decode_b64(encoded_str).decode('utf-8')
    assert actual_val == expected_val

def test_if_exception_thrown_if_data_is_not_binary(encoder_obj):
    with pytest.raises(ValueError):
        data = "abcd"
        encoder_obj.encode_b64(data)

def test_if_tar_file_being_converted_to_binary(encoder_obj):
    file_path = os.path.abspath('tests/utilities/69.tar.gz')
    binary_data = encoder_obj.download_package_binary(file_path)
    assert type(binary_data) == bytes

def test_exception_thrown_if_file_not_found(encoder_obj):
    with pytest.raises(FileNotFoundError):
        file_path = os.path.abspath('tests/utilities/68.tar.gz')
        _ = encoder_obj.download_package_binary(file_path)
