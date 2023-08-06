from urllib.parse import urlparse

from vk_urls_validator.utils import exceptions, utils

MAIN_HOST = 'vk.com'
POSSIBLE_HOSTS = ['vk.com', 'm.vk.com', 'vk.ru']


def validate_url(url: str) -> str:
    """
    Validate VK URL

    Parameters:
        url (``str``):
            Url to validate

    Returns:
        :obj:`str`: validated URL

    Raises:
        CantFindHostnameError:
            Can't find URL's hostname.

        HostNotInPossibleHostsError:
            URL's host not in possible hosts.

        VKInvalidHashError:
            URL's hash does not comply with VK rules.
    """
    if url.startswith('https://') or url.startswith('http://'):
        parsed_url = urlparse(url=url)
    else:
        parsed_url = urlparse(url=f'https://{url}')

    if parsed_url.hostname is None:
        raise exceptions.CantFindHostnameError(url=url)

    hostname = utils.get_hostname(hostname=parsed_url.hostname, hostnames=POSSIBLE_HOSTS)
    if hostname is None:
        raise exceptions.HostNotInPossibleHostsError(url=url, possible_hosts=POSSIBLE_HOSTS)

    url_hash = utils.validate_hash(url=url, url_hash=parsed_url.path)

    return f'https://vk.com/{url_hash}'
