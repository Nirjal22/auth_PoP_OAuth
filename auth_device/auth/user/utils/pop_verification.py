import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

def verify_signature(public_key_pem, signature_b64, message: bytes):
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode()
    )
    signature = base64.b64decode(signature_b64)

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except (ValueError, InvalidSignature):
        return False
