import re
from typing import Dict

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
            "Download",
            "download",
        ]
        for title, url in urls:
            if _ := self.gh_pattern(pattern, url) and title in possible_keys:
                return url

    def licenses(self, raw_data: Dict) -> str:
        licenses = raw_data["license"]
        if licenses != "" and licenses is not None:
            return licenses
        licenses_pattern = r"^[lL]icense.*"

        for lic in raw_data["classifiers"]:
            if license_found := re.search(licenses_pattern, lic):
                return license_found.group()

    def project_url(self, pattern: str, project_url: str, project_urls: Dict) -> str:
        if project_url != "" and self.gh_pattern(pattern, project_url):
            return project_url

        if project_urls:
            logger.debug("Nested metadata found")
            return self.additional_urls(pattern, project_urls)

    def version(self, version: str, pattern: str, filtered_data: Dict) -> Dict:
        project_default_error = "No project url found, please check manually"
        if version and self.gh_pattern(
            pattern, filtered_data.get("project_url"), project_default_error
        ):
            filtered_data[
                "version_url"
            ] = f"{filtered_data['project_url']}/tree/{version}/"

        else:
            version_default_error = "No version url found, please check manually"
            filtered_data["version_url"] = version_default_error

        return filtered_data
