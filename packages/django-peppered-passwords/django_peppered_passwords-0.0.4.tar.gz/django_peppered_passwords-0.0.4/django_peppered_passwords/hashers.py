from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.crypto import pbkdf2
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class PepperedPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    algorithm = "pbkdf2_sha256_with_pepper"

    def __init__(self) -> None:
        super().__init__()

        if not hasattr(settings, "PEPPERED_PASSWORDS_SECRET_KEY"):
            raise ImproperlyConfigured("PEPPERED_PASSWORDS_SECRET_KEY should be defined in django settings.")

    def encode(self, password, salt, iterations=None):
        iterations = iterations or self.iterations
        hash = pbkdf2(password, salt + settings.PEPPERED_PASSWORDS_SECRET_KEY, iterations, digest=self.digest)
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash.hex())
