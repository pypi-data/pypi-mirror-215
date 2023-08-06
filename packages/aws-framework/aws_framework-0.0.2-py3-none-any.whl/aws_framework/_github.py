from botocore.utils import random

from ._config import cfg
from ._types import *
from .client import ApiClient


class GithubClient(ApiClient):
    def __init__(self, token: Optional[str] = None):
        if token is None:
            self.headers = {
                "Authorization": "token " + cfg.GH_API_TOKEN,
                "Accept": "application/vnd.github.v3+json",
            }
        else:
            self.headers = {
                "Authorization": "token " + token,
                "Accept": "application/vnd.github.v3+json",
            }
        super().__init__()
        self.base_url = "https://api.github.com"

    async def search_repos(self, query: str, login: str) -> List[GithubRepo]:
        response = await self.fetch(
            f"/search/repositories?q={query}+user:{login}&sort=stars&order=desc"
        )
        assert isinstance(response, dict)
        return [GithubRepo(**repo) for repo in response["items"]]

    async def create_repo(self, repo: CreateRepo) -> GitHubRepoFull:
        response = await self.fetch(
            "/user/repos",
            method="POST",
            json=repo.dict(),
        )
        assert isinstance(response, dict)
        return GitHubRepoFull(**response)

    async def create_repo_from_template(self, body: RepoTemplateCreate):
        return await self.fetch(
            f"/repos/{body.template_owner}/{body.template_repo}/generate",
            "POST",
            json={
                "owner": body.login,
                "name": body.name,
                "description": f"Automatically generated {body.template_repo} template by BlackBox API made with ❤️ by @{body.template_owner}",
            },
        )
