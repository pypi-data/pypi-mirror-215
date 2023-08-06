from axsqlalchemy.uow import BaseRepoCollector

from .user import UserReposity


class RepoCollector(BaseRepoCollector):
    user: UserReposity
