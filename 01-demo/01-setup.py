# Create a data key identified in the key vault collection demo.keyvault.
import base64
import os

from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from bson import binary
from bson.codec_options import CodecOptions

codec_opts = CodecOptions(uuid_representation=binary.STANDARD)

# Test key material generated by: echo $(head -c 96 /dev/urandom | base64 | tr -d '\n')
if "LOCAL_DATAKEY_BASE64" not in os.environ:
    raise Exception("Set LOCAL_DATAKEY_BASE64 env variable to 96 bytes of base64")

masterkey = binary.Binary(base64.b64decode(os.environ["LOCAL_DATAKEY_BASE64"]))
kms_providers = {"local": {"key": masterkey}}
client = MongoClient("mongodb://localhost:27017/")
# Reset the collection
client.demo.keyvault.drop()
client_encryption = ClientEncryption(
    kms_providers, "demo.keyvault", client, codec_opts)
key_uuid = client_encryption.create_data_key("local")

# Store the key id into a file for easy access.
open("key_uuid.txt", "w").write(base64.b64encode(key_uuid).decode("utf-8"))

print("Created data key in demo.keyvault with UUID: %s" % key_uuid.hex())
print("Proceed to 02-roundtrip.py")
