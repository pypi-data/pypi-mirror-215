import requests
from loguru import logger

from lemmy.auth import Authentication
from lemmy.admin import Admin
from lemmy.comment import Comment
from lemmy.community import Community
from lemmy.modlog import Modlog
from lemmy.post import Post
from lemmy.private_message import PrivateMessage
from lemmy.search import Search
from lemmy.site import Site
from lemmy.user import User

class Lemmy:
    admin: Admin
    comment: Comment
    community: Community
    modlog: Modlog
    post: Post
    private_message: PrivateMessage
    search: Search
    site: Site
    user: User
    _auth: Authentication
    _known_communities = {}

    def __init__(self, api_base_url: str) -> None:
        self._auth = Authentication()
        self.admin = Admin()
        self._auth.api_base_url = f"{api_base_url}/api/v3"
        self.comment = Comment()
        self.community = Community()
        self.modlog = Modlog()
        self.post = Post()
        self.private_message = PrivateMessage()
        self.search = Search()
        self.site = Site()
        self.user = User()

    def log_in(self, username_or_email: str, password: str) -> bool:
        return Authentication().log_in(username_or_email, password)
    
    def log_out(self) -> bool:
        return Authentication().log_out()

    def discover_community(self, community_name: str) -> int | None:
        if community_name in self._known_communities:
            return self._known_communities[community_name]
        try:
            req = requests.get(f"{self._auth.api_base_url}/community?name={community_name}")
            community_id = req.json()["community_view"]["community"]["id"]
            self._known_communities[community_name] = community_id
        except Exception as err:
            logger.error(f"Error when looking up community '{community_name}': {err}")
            return
        return community_id
