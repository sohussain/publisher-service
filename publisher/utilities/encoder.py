"""
@discription: Encoder class is responsible for
encoding/decoding binary data to base64
@author: abdullahrkw
"""
import base64
import io
import logging
import os
import tarfile


class Encoder:
    def download_package_binary(self, file):
        if (os.path.isfile(file)):
            try:
                with open(file, 'rb') as f:
                    return f.read()
            except Exception as e:
                logging.error(
                    f"Couldn't read tarfile at {file} with error {e}")
                raise RuntimeError(f"Couldn't read tarfile at {file}")

        else:
            raise FileNotFoundError(f"Couldn't find file {file}")

    def encode_b64(self, binary_data):
        try:
            encoded_string = base64.b64encode(binary_data)
            return encoded_string
        except Exception as e:
            logging.error(f"Couldn't encode package with error: {e}")
            raise ValueError(f"Couldn't encode package with error: {e}")

    def decode_b64(self, encoded_string):
        try:
            decoded_binary_data = base64.b64decode(encoded_string)
        except Exception as e:
            logging.error(f"Couldn't decode package with error: {e}")
        return decoded_binary_data
