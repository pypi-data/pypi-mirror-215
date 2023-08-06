from typing import List, Optional

from vk_urls_validator.utils import exceptions
import string

ALLOWED_CHARACTERS = string.digits + string.ascii_uppercase + string.ascii_lowercase + '._'


def get_hostname(hostname: str, hostnames: List[str]) -> Optional[str]:
    for prefix in hostnames:
        if hostname.startswith(prefix):
            return prefix
    return None


def validate_hash(url: str, url_hash: str) -> Optional[str]:
    """
    Hash validating by VK rules (https://vk.com/faq18038)

    :param url: URL
    :param url_hash: URL hash
    :return:
    """

    url_hash = url_hash.strip('/').strip()

    if url_hash.startswith('id') and url_hash[2:].isnumeric():
        return url_hash

    if url_hash.startswith('public') and url_hash[6:].isnumeric():
        return url_hash

    if url_hash.startswith('club') and url_hash[5:].isnumeric():
        return url_hash

    return url_hash

    # if not 5 <= len(url_hash) <= 32:
    #     raise exceptions.VKInvalidHashError(url=url)
    #
    # if url_hash[:3].isnumeric():
    #     raise exceptions.VKInvalidHashError(url=url)
    #
    # if url_hash.startswith('_') or url_hash.endswith('_'):
    #     raise exceptions.VKInvalidHashError(url=url)
    #
    # for i in range(len(url_hash)):
    #     if url_hash[i] not in ALLOWED_CHARACTERS:
    #         raise exceptions.VKInvalidHashError(url=url)
    #
    # characters = set(url_hash)
    # if characters.discard(set(ALLOWED_CHARACTERS)):
    #     raise exceptions.VKInvalidHashError(url=url)
    #
    # return url_hash
