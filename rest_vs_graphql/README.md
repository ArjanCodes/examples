# Introduction

In this video, I'm going to talk about API design. I'll start with the basics of REST and then move on to GraphQL.

# Show example of building a simple REST interface with Flask (screencast)

# Problems with the REST interface (talking head)

- You kind of have to make sure yourself that the REST interface adheres to the standard.
- Getting the author of a blog requires a separate request. You could implement a population mechanism, but there's no standard way to do that.
- There's no distinction between data in the database and the structure of the data in the REST interface. From a data separation point of view, this would be nice. But again, there's no standard way to do that in REST. A related issue is that because there's no separation, you might accidentally send back information you don't want to be public. Such as a user's email address or password. As a result, you need to explicitly block these things in the REST interface.
- There's no way to control how much data you get back from a request. Blogs are not that big, but if you have a document with a lot of fields, you might want to control this in some way. You could add something for that, but again, there's no standard way to do that in REST.

# Enter GraphQL (talking head)

As opposed to REST, which has multiple endpoints and uses various HTTP verbs to interact with the server (GET, POST, DELETE, etc), GraphQL uses a query language to interact with the server, and a single endpoint.

GraphQL has standard solutions for many of the problems with REST. For example, GraphQL allows you to specify exactly what data you get back from a request, you can do things like get the author of the blog in a single request, and you can define the structure of the data using a GraphQL schema. If you try to get something that's not specified in the GraphQL schema, you'll get an error.

# Create a simple GraphQL interface (screencast)

# Some cons of GraphQL (talking head)

- With GraphQL, sending a request to the server is a bit more complicated than with a REST interface, since you have to specify the query or mutation you want to make.

- GraphQL suffers from the n+1 problem. If you retrieve a bunch of blogs with authors, a separate database request will be made for each author, which potentially slows things down.

- The GraphQL language is verbose in some cases. For example, specifying a mutation is a pain. I think this should be shortened.

- Not everything in GraphQL is standardized. For example, it would be nice to have a standard way to do search and pagination (with page sizes and results, or using cursors). Also, having standard options for authentication, roles, and permissions, would be a great improvement.

# Updating a blog (REST)

curl -X POST -H "Content-Type: application/json" \
 -d '{"title": "I like this blog" }' \
 http://127.0.0.1:5000/blogs/1

# Updating a blog (GraphQL)

Below is an example of a GraphQL mutation for updating a blog

mutation UpdateBlog($id: ID!, $payload: BlogPayload!) {
update_blog(id: $id, payload: $payload) {
id
title
content
}
}

Variables:

{
"id":1,
"payload": {
"title":"Hello this is a blog"
}
}
