# vk_urls_validator

Library for validating VK urls and brings them to one standart.

# How method works?

1. Add prefix "https://"
2. Change all hostnames to "vk.com"
3. Check URL hash for VK rules


# Examples

```python
from vk_urls_validator import validate_url

validated_url = validate_url(url='vk.com/id1')
# >> https://vk.com/id1

validated_url = validate_url(url='https://m.vk.com/id1')
# >> https://vk.com/id1
```


# Installing

```commandline
pip3 install vk_urls_validator
```
