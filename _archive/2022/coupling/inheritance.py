from typing import Any

from elasticsearch import Elasticsearch
from requests_aws4auth import AWS4Auth


class Elastic(Elasticsearch):
    def __init__(self, index_name: str, host: str) -> None:
        awsauth = AWS4Auth(
            service="elb",
        )
        super().__init__(
            hosts=[host],
            http_auth=awsauth,
            verify_certs=True,
        )
        self.index_name = index_name

    def find_hits(
        self,
        query: dict[str, Any],
        size: int,
        index: str,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        response = self.search(
            query=query,
            size=size,
            index=index or self.index_name,
            **kwargs,
        )
        return response["hits"]["hits"]


class DevElastic(Elastic):
    def __init__(self, index_name: str) -> None:
        super().__init__(
            host="localhost:8700",
            index_name=index_name,
        )
