import hashlib
from rest_framework.permissions import BasePermission
from ..models import Device
from .pop_verification import verify_signature

class ProofOfPossessionPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            pop_key = Device.objects.get(user=user)
        except Device.DoesNotExist:
            return False

        signature = request.headers.get("X-PoP-Signature")
        timestamp = request.headers.get("X-PoP-Timestamp")

        if not signature or not timestamp:
            return False

        body_hash = hashlib.sha256(request.body or b"").hexdigest()

        message = (
            f"{request.method}\n"
            f"{request.path}\n"
            f"{timestamp}\n"
            f"{body_hash}"
        ).encode()

        return verify_signature(
            pop_key.public_key_pem,
            signature,
            message,
        )
