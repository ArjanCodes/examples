from ariadne import MutationType, QueryType

MAIN_TYPEDEF = """
    type Query {
        blogs: [Blog]!
        blog(id: ID!): Blog!
        authors: [Author]!
        author(id: ID!): Author!
    }
    """

query = QueryType()
mutation = MutationType()
