"""
This type stub file was generated by pyright.
"""

import sys
import re
import unicodedata
import dns.resolver
import dns.exception
import idna

ALLOW_SMTPUTF8 = ...
CHECK_DELIVERABILITY = ...
TEST_ENVIRONMENT = ...
GLOBALLY_DELIVERABLE = ...
DEFAULT_TIMEOUT = ...
ATEXT = ...
DOT_ATOM_TEXT = ...
ATEXT_INTL = ...
DOT_ATOM_TEXT_INTL = ...
ATEXT_HOSTNAME = ...
EMAIL_MAX_LENGTH = ...
LOCAL_PART_MAX_LENGTH = ...
DOMAIN_MAX_LENGTH = ...
SPECIAL_USE_DOMAIN_NAMES = ...
if sys.version_info >= (3, ):
    unicode_class = str
else:
    ...
class EmailNotValidError(ValueError):
    """Parent class of all exceptions raised by this module."""
    ...


class EmailSyntaxError(EmailNotValidError):
    """Exception raised when an email address fails validation because of its form."""
    ...


class EmailUndeliverableError(EmailNotValidError):
    """Exception raised when an email address fails validation because its domain name does not appear deliverable."""
    ...


class ValidatedEmail:
    """The validate_email function returns objects of this type holding the normalized form of the email address
    and other information."""
    original_email = ...
    email = ...
    local_part = ...
    domain = ...
    ascii_email = ...
    ascii_local_part = ...
    ascii_domain = ...
    smtputf8 = ...
    mx = ...
    mx_fallback_type = ...
    def __init__(self, **kwargs) -> None:
        ...
    
    def __self__(self):
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def __getitem__(self, key): # -> None:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def as_constructor(self): # -> str:
        ...
    
    def as_dict(self): # -> dict[str, Any]:
        ...
    


def caching_resolver(*, timeout=..., cache=...): # -> Resolver:
    ...

def validate_email(email, *, allow_smtputf8=..., allow_empty_local=..., check_deliverability=..., test_environment=..., globally_deliverable=..., timeout=..., dns_resolver=...): # -> ValidatedEmail:
    """
    Validates an email address, raising an EmailNotValidError if the address is not valid or returning a dict of
    information when the address is valid. The email argument can be a str or a bytes instance,
    but if bytes it must be ASCII-only.
    """
    ...

def validate_email_local_part(local, allow_smtputf8=..., allow_empty_local=...): # -> dict[str, Unknown | bool] | dict[str, str | bool | None]:
    ...

def validate_email_domain_part(domain, test_environment=..., globally_deliverable=...): # -> dict[str, str]:
    ...

def validate_email_deliverability(domain, domain_i18n, timeout=..., dns_resolver=...):
    ...

def main(): # -> None:
    ...

if __name__ == "__main__":
    ...