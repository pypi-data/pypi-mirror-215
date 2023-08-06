from dataclasses import dataclass

from typing_extensions import Literal

from twitter_api.types.http import Url

EndpointMethod = Literal["GET", "POST", "DELETE"]


@dataclass(frozen=True)
class Endpoint:
    method: EndpointMethod
    url: Url
