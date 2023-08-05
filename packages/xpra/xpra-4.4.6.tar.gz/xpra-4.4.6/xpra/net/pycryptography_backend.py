# This file is part of Xpra.
# Copyright (C) 2011-2021 Antoine Martin <antoine@xpra.org>
# Copyright (C) 2008, 2009, 2010 Nathaniel Smith <njs@pobox.com>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

#this is a loader module, designed to import things on-demand:
#pylint: disable=import-outside-toplevel

import os

from xpra.os_util import strtobytes, memoryview_to_bytes
from xpra.log import Logger

log = Logger("network", "crypto")

__all__ = ("get_info", "get_key", "get_encryptor", "get_decryptor", "ENCRYPTION_CIPHERS", "MODES")

DEFAULT_MODE = os.environ.get("XPRA_CRYPTO_MODE", "CBC")

ENCRYPTION_CIPHERS = []
MODES = tuple(x for x in os.environ.get("XPRA_CRYPTO_MODES", "CBC,GCM,CFB,CTR").split(",")
              if x in ("CBC", "GCM", "CFB", "CTR"))
KEY_HASHES = ("SHA1", "SHA224", "SHA256", "SHA384", "SHA512")
KEY_STRETCHING = ("PBKDF2", )
backend = None


def patch_crypto_be_discovery():
    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller / cx_freeze / pyexe / py2app freezing.
    """
    from cryptography.hazmat import backends
    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        log("failed to import commoncrypto", exc_info=True)
        be_cc = None
    try:
        import _ssl
        log("loaded _ssl=%s", _ssl)
    except ImportError:
        log("failed to import _ssl", exc_info=True)
        be_ossl = None
    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        log("failed to import openssl backend", exc_info=True)
        be_ossl = None
    setattr(backends, "_available_backends_list", [
        be for be in (be_cc, be_ossl) if be is not None
    ])

def init():
    import sys
    from xpra.os_util import OSX
    if getattr(sys, 'frozen', False) or OSX:
        patch_crypto_be_discovery()
    global backend, ENCRYPTION_CIPHERS
    import cryptography
    assert cryptography
    from cryptography.hazmat.backends import default_backend
    backend = default_backend()
    log("default_backend()=%s", backend)
    log("backends=%s", getattr(backend, "_backends", []))
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import hashes
    assert Cipher and algorithms and modes and hashes
    ENCRYPTION_CIPHERS[:] = ["AES"]

def get_info():
    import cryptography
    return {"backend"                       : "python-cryptography",
            "python-cryptography"           : {
                ""          : True,
                "version"   : cryptography.__version__,
                }
            }

def get_key(password, key_salt, key_hash, block_size, iterations):
    global backend
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    assert key_hash.upper() in KEY_HASHES, "invalid key hash %s, should be one of %s" % (key_hash.upper(), KEY_HASHES)
    algorithm = getattr(hashes, key_hash.upper(), None)
    assert algorithm, "%s not found in cryptography hashes" % key_hash.upper()
    try:
        #newer versions (41 for sure) require us to instantiate the "constant"
        hash_algo = algorithm()
    except TypeError:
        #older versions are OK using it directly:
        hash_algo = algorithm
    kdf = PBKDF2HMAC(algorithm=hash_algo, length=block_size,
                     salt=strtobytes(key_salt), iterations=iterations, backend=backend)
    key = kdf.derive(strtobytes(password))
    return key

def _get_cipher(key, iv, mode=DEFAULT_MODE):
    global backend
    assert mode in MODES
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    mode_class = getattr(modes, mode, None)
    if mode_class is None:
        raise ValueError("no %s mode in this version of python-cryptography" % mode)
    return Cipher(algorithms.AES(key), mode_class(strtobytes(iv)), backend=backend)

def get_block_size(mode):
    if mode=="CBC":
        #16 would also work,
        #but older versions require 32
        return 32
    return 0

def get_encryptor(key, iv, mode=DEFAULT_MODE):
    encryptor = _get_cipher(key, iv, mode).encryptor()
    encryptor.encrypt = encryptor.update
    return encryptor

def get_decryptor(key, iv, mode=DEFAULT_MODE):
    decryptor = _get_cipher(key, iv, mode).decryptor()
    def i(s):
        try:
            return int(s)
        except ValueError:
            return 0
    import cryptography
    version = cryptography.__version__
    supports_memoryviews = tuple(i(s) for s in version.split("."))>=(2, 5)
    log("get_decryptor(..) python-cryptography supports_memoryviews(%s)=%s",
        version, supports_memoryviews)
    if supports_memoryviews:
        decryptor.decrypt = decryptor.update
    else:
        _patch_decryptor(decryptor)
    return decryptor

def _patch_decryptor(decryptor):
    #with older versions of python-cryptography,
    #we have to copy the memoryview to a bytearray:
    def decrypt(v):
        return decryptor.update(memoryview_to_bytes(v))
    decryptor.decrypt = decrypt


def main():
    from xpra.platform import program_context
    from xpra.util import print_nested_dict
    import sys
    if "-v" in sys.argv or "--verbose" in sys.argv:
        log.enable_debug()
    with program_context("Encryption Properties"):
        init()
        print_nested_dict(get_info())


if __name__ == "__main__":
    main()
