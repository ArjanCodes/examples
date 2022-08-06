import os
from enum import Enum
from typing import Any

from boto3 import Session
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from .env import getenv


class Host(str, Enum):
    DEV = "DEV"
    IAC = "IAC"
    REI = "REI"


class Elastic(Elasticsearch):
    def __init__(
        self,
        index_name: str | None = None,
        host: str | None = None,
    ) -> None:
        host = host or getattr(self, "host", None) or os.getenv("ES_HOST")  # noqa: B009
        if not host:
            raise TypeError("Argument 'host' must be provided.")
        keys = os.getenv("AWS_ACCESS_KEY"), os.getenv("AWS_SECRET_KEY")
        awsauth = AWS4Auth(
            region="eu-west-3",
            service="elb",
            refreshable_credentials=Session(*keys).get_credentials(),
        )
        super().__init__(
            hosts=[host],
            http_auth=awsauth,
            use_ssl=False,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )
        self.index_name = index_name

    @classmethod
    def with_host(
        cls,
        host: Host,
        index_name: str | None = None,
        *,
        maxsize: int = 32,
        timeout: int = 10,
    ) -> Elastic:
        return cls(
            host=f"{get_host(host)}.eu-west-3.elb.amazonaws.com:9200",
            index_name=index_name,
            maxsize=maxsize,
            timeout=timeout,
        )

    def find(
        self,
        query: dict[str, Any] | None = None,
        size: int = 1,
        index: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self.search(
            query=query,
            size=size,
            index=index or self.index_name,
            **kwargs,
        )

    def find_hits(
        self,
        query: dict[str, Any] | None = None,
        size: int = 1,
        index: str | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        response = self.find(
            query=query,
            size=size,
            index=index or self.index_name,
            **kwargs,
        )
        return response["hits"]["hits"]


class DevElastic(Elastic):
    @property
    def host(self) -> str:
        return f"{get_host(Host.DEV)}.eu-west-3.elb.amazonaws.com:9200"


def get_host(name: str) -> str:
    if not (host := getenv(f"MX_ELASTIC_AWS_{name}")):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return host
