import re

from extractor.logger import logger


class StandardCheck:
    def gh_pattern(self, pattern: str, url: str, custom_error: str = None):
        try:
            found = re.search(pattern, url)
        except Exception as e:
            logger.warning(custom_error) if custom_error else logger.warning(e)
        else:
            return found

    def additional_urls(self, pattern: str, project_urls: str):
        urls = project_urls.items()
        possible_keys = [
            "Code",
            "Source Code",
            "Source code",
            "Source",
            "Homepage",
            "Home",
            "Repository",
            "repository",
        ]
        for title, url in urls:
            if _ := self.gh_pattern(pattern, url) and title in possible_keys:
                return url

    def version(
        self, version: str, pattern: str, raw_data: dict, filtered_data: dict
    ) -> dict:
        project_default_error = "No project url found, please check manually"
        version_default_error = "No version url found, please check manually"
        if version and self.gh_pattern(
            pattern, filtered_data.get("project_url"), project_default_error
        ):
            filtered_data[
                "version_url"
            ] = f"{filtered_data['project_url']}/tree/{version}/"
        elif raw_data["release_url"] and self.gh_pattern(
            pattern, filtered_data.get("project_url"), version_default_error
        ):
            filtered_data["version_url"] = raw_data["release_url"]

        else:
            filtered_data["version_url"] = version_default_error
            filtered_data["project_url"] = project_default_error
        return filtered_data
