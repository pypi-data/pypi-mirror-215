import re

from loguru import logger


class StandardCheck:
    def gh_pattern(self, pattern: str, url: str):
        try:
            found = re.search(pattern, url)
        except Exception as e:
            logger.error(e)
        else:
            return found

    def additional_urls(self, pattern: str, project_urls: str):
        urls = project_urls.items()
        possible_keys = [
            "Source Code",
            "Source",
            "Homepage",
            "Home",
            "Repository",
            "repository",
        ]
        for title, url in urls:
            if _ := self.gh_pattern(pattern, url) and title in possible_keys:
                return url
