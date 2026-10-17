import base64
import os
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes

from nexus_c2.core.models import EncryptedEnvelope, EnvelopeHeader


class EnvelopeCryptoEngine:
    """Zero-Trust Envelope Encryption Engine (AES-256-GCM + DEK/KEK Pattern)."""

    def __init__(self, master_key: Optional[bytes] = None) -> None:
        # Key Encryption Key (KEK) - Master Key
        self.kek = master_key or AESGCM.generate_key(bit_length=256)
        self.key_fingerprint = base64.b64encode(hashes.Hash(hashes.SHA256()).update(self.kek) or b"").decode("utf-8")[:16]

    def encrypt_payload(
        self, message_id: str, sender_id: str, recipient_id: str, payload: Dict[str, Any]
    ) -> EncryptedEnvelope:
        """Szyfruje dane wiadomości z użyciem unikalnego klucza symetrycznego (DEK)."""
        # 1. Generowanie jednorazowego Data Encryption Key (DEK)
        dek = AESGCM.generate_key(bit_length=256)
        
        # 2. Szyfrowanie ładunku (Payload) za pomocą DEK
        aesgcm_dek = AESGCM(dek)
        nonce = os.urandom(12)
        plaintext = json.dumps(payload).encode("utf-8")
        
        # AESGCM.encrypt zwraca ciphertext + auth_tag (ostatnie 16 bajtów)
        encrypted_raw = aesgcm_dek.encrypt(nonce, plaintext, None)
        ciphertext = encrypted_raw[:-16]
        tag = encrypted_raw[-16:]

        # 3. Szyfrowanie klucza DEK za pomocą Master Key (KEK)
        aesgcm_kek = AESGCM(self.kek)
        dek_nonce = os.urandom(12)
        encrypted_dek_raw = aesgcm_kek.encrypt(dek_nonce, dek, None)

        # 4. Pakowanie do bezpiecznej koperty
        header = EnvelopeHeader(
            message_id=message_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            key_fingerprint=self.key_fingerprint,
        )

        return EncryptedEnvelope(
            header=header,
            encrypted_dek=base64.b64encode(dek_nonce + encrypted_dek_raw).decode("utf-8"),
            nonce=base64.b64encode(nonce).decode("utf-8"),
            ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
            tag=base64.b64encode(tag).decode("utf-8"),
        )

    def decrypt_envelope(self, envelope: EncryptedEnvelope) -> Dict[str, Any]:
        """Odszyfrowuje bezpieczną kopertę i weryfikuje spójność danych (Zero-Trust)."""
        # 1. Odszyfrowanie klucza DEK za pomocą KEK
        encrypted_dek_combined = base64.b64decode(envelope.encrypted_dek)
        dek_nonce = encrypted_dek_combined[:12]
        encrypted_dek_bytes = encrypted_dek_combined[12:]

        aesgcm_kek = AESGCM(self.kek)
        dek = aesgcm_kek.decrypt(dek_nonce, encrypted_dek_bytes, None)

        # 2. Odszyfrowanie właściwego ładunku z użyciem odszyfrowanego DEK
        nonce = base64.b64decode(envelope.nonce)
        ciphertext = base64.b64decode(envelope.ciphertext)
        tag = base64.b64decode(envelope.tag)

        aesgcm_dek = AESGCM(dek)
        plaintext = aesgcm_dek.decrypt(nonce, ciphertext + tag, None)

        return json.loads(plaintext.decode("utf-8"))