import subprocess
from typing import List

from openapi_client import ResponseGitHubCodeRef
from vessl import logger
from vessl.util.downloader import Downloader


def clone_codes(code_refs: List[ResponseGitHubCodeRef]):
    for code_ref in code_refs:
        if code_ref.git_provider == "github":
            prefix = "x-access-token"
            git_provider_domain = "github.com"
        elif code_ref.git_provider == "gitlab":
            prefix = "oauth2"
            git_provider_domain = "gitlab.com"
        else:
            prefix = "x-token-auth"
            git_provider_domain = "bitbucket.org"

        if code_ref.git_provider_custom_domain is not None:
            git_provider_domain = code_ref.git_provider_custom_domain

        if code_ref.token is None or code_ref.token == "":
            git_url = f"https://{git_provider_domain}/{code_ref.git_owner}/{code_ref.git_repo}.git"
        else:
            git_url = f"https://{prefix}:{code_ref.token}@{git_provider_domain}/{code_ref.git_owner}/{code_ref.git_repo}.git"
        if code_ref.mount_path:
            dirname = code_ref.mount_path
        else:
            dirname = code_ref.git_repo

        try:
            subprocess.run(["git", "clone", git_url, dirname])
        except subprocess.CalledProcessError:
            dirname = f"vessl-{code_ref.git_repo}"
            logger.info(f"Falling back to '{dirname}'...")
            subprocess.run(["git", "clone", git_url, dirname])

        if code_ref.git_ref:
            subprocess.run(["/bin/sh", "-c", f"cd {dirname}; git reset --hard {code_ref.git_ref}"])

        if code_ref.git_diff_file:
            diff_file_path = f"/tmp/{code_ref.git_repo}.diff"
            Downloader.download(
                code_ref.git_diff_file.path, diff_file_path, code_ref.git_diff_file, quiet=False
            )
            subprocess.run(["/bin/sh", "-c", f"cd {dirname}; git apply {diff_file_path}"])
