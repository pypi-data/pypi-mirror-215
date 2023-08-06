# Django peppered passwords

Adds a secret private key to the hashed passwords created with django.contrib.auth.

## Configuration

Define a secret in your project's settings.

    PEPPERED_PASSWORDS_SECRET_KEY = 'b04ab0b2d1e69cfa54f49f348c3388c2e6017cae6c5aefa4'

Do not use the secret key in example. Create your own.

Create a secret key by using python's builtin secret module.

    >>> import secrets
    >>> secrets.token_bytes(32).hex()

Add the hasher `PASSWORD_HASHERS` in your projects settings file. `PASSWORD_HASHERS` comes from Django.

    PASSWORD_HASHERS = [
      "django_peppered_passwords.hashers.PepperedPBKDF2PasswordHasher"
    ]

Please take it to the consideration, this is an irreversible action. Switching from peppered hashing to Django's default hasher is not possible.

Once you update the secret key, all the passwords will be broken. The users will need to reset their passwords via email.

## Background

Currently a user's password stored in database in this format:

     <algorithm>$<iterations>$<salt>$<hash>

Hash (Last column) is the password hashed with the salt in previous column. Example, these are two computed passwords, stored on database, for the same password of two users.

    pbkdf2_sha256$600000$fb9cUsHWK4EMZ7VWGBAcGD$2uwiVefFwanIhxLrv+/t3sKvP4X6tDKEMw/ysHD5dIc=
    pbkdf2_sha256$600000$HgWHWrF2qQD9Owj4XeEkjY$rh0qzfo+/ZCzWbL9ZJa8aKhiO5xoEMfT4EtP/+A+LzI=

The password is 123456. Imagine I am an attacker, who got the database of different django project, I want to look up the users who have chosen the password 123456. I have the salts of users stored in database.

    >>> make_password('123456', 'fb9cUsHWK4EMZ7VWGBAcGD')
    pbkdf2_sha256$600000$fb9cUsHWK4EMZ7VWGBAcGD$2uwiVefFwanIhxLrv+/t3sKvP4X6tDKEMw/ysHD5dIc=
    >>> make_password('123456', 'HgWHWrF2qQD9Owj4XeEkjY')
    pbkdf2_sha256$600000$HgWHWrF2qQD9Owj4XeEkjY$rh0qzfo+/ZCzWbL9ZJa8aKhiO5xoEMfT4EtP/+A+LzI=

These are correct password combinations. I am able to lookup the users who have their passwords exposed in public. Password 123456 is not a possible case in Django, since the password fields have a complexity validation. However, the salt is available to the attacker when a database is stolen. Salt could be used

- To hash the raw password pair in a rainbow table.
- To hash the already exposed passwords.

There is one more element needed for hashing the password, pepper, should be project specific. When a database is exposed in public, the attacker will not be able to lookup the passwords, since they don't have the secret pepper key.

## Notes from Django ticket 30561

According to NIST Digital Identity Guidelines Authentication and Lifecycle Management document, verifiers should perform an additional iteration of a key derivation function using a salt value that is secret and known only to the verifier.

- <https://code.djangoproject.com/ticket/30561>
- <https://pages.nist.gov/800-63-3/sp800-63b.html>
