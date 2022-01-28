from ariadne import make_executable_schema
from graphql.type.schema import GraphQLSchema

from schema.author import AUTHOR_TYPEDEF
from schema.blog import BLOG_TYPEDEF, blog_query
from schema.types import MAIN_TYPEDEF, mutation, query


def create_schema() -> GraphQLSchema:
    return make_executable_schema(
        [MAIN_TYPEDEF, BLOG_TYPEDEF, AUTHOR_TYPEDEF], [query, blog_query, mutation]
    )
