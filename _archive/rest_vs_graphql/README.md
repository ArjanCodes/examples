# Introduction

REST vs GraphQL. I know what you're thinking. Ah, this is one of those videos again where we're supposed to find out which one is better. But then it becomes a lame "it depends on what you want to use it for".

So which one is better? Well, IT DEPENDS. You know why? Because we're nuanced people. The world of software development is not black and white. It's 254 shades of grey. Fifty... pfft, amateurs.

So, we are going to dive into the details. Talk about some pros and cons of REST and GraphQL, show you a couple of examples. And then give you some of my thoughts on when to use one over the other.

Before we dive in, let's first talk about the sponsor of this video, Skillshare.

(skillshare section)

REST itself is already quite old. It was originated in 2000 by Roy Fielding in his PhD thesis "Architectural Styles and the Design of Network-based Software Architectures".

"REST" stands for Representational State Transfer. The basic idea is that when you want to take some action on a resource, the HTTP request body contains the desired new state, and the server will then reply with the actual state after handling the request. REST interface are therefore resource-oriented. This is different from RPC style interfaces, which are action-oriented. You call a remote function, that performs a certain task and you get the result back. For example, you could have a RPC "setBlogTitle('My title')" and get back "OK".

Let's look at how we can create a simple REST API in Python.

# Show example of building a simple REST interface with Flask (screencast)

# Problems with the REST interface (talking head)

Let's talk about some of the problems with the REST interface. If you're enjoying the video so far, give it a thumbs up. That helps spread the word about this channel.

- You kind of have to make sure yourself that the REST interface adheres to the standard. A good starting point to help you with this is Swagger and the OpenAPI standard. They also provide tools to help you design your APIs while making sure they adhere to the standard. I'll put a link to Swagger in the description of the video.

https://swagger.io

- Getting the author of a blog requires a separate request. You could implement a population mechanism, but there's no standard way to do that. This leads to having to coordinate several requests in the frontend to get the data you need and waiting for them to complete, slowing down the user experience.

- REST doesn't enforce a distinction between the structure of the data in the database and the structure of the data that you receive and send via the API. This invites developers to just directly send back data retrieved from the database, leading to security issues. For example, you might accidentally send back information you don't want to be public. Such as a user's email address or password. If you're not careful, it's really easy to make mistakes.

- There's no way to control how much data you get back from a request. Blogs are not that big, but if you have a document with a lot of fields, you might want to control this in some way. You could add something for that, but again, there's no standard way to do that in REST.

# Enter GraphQL (talking head)

As opposed to REST, which has multiple endpoints and uses various HTTP verbs to interact with the server (GET, POST, DELETE, etc), GraphQL uses a query language to interact with the server, and a single endpoint. The QL in GraphQL stands for query language. But what about the Graph? Basically, the difference between REST and GraphQL is that GraphQL views data as a graph structure: objects are connected by relationships, forming a graph structure.

This is combined with a query language, which allows you to specify exactly what data you want to get back from the server and more specifically, which parts of the graph structure you want to retrieve. As opposed to REST, getting the blog posts and associated authors is handled in a single request.

Furthermore, you define the interface with the GraphQL backend, via a schema, specifying exactly what the data looks like. And this solves a lot of security issues. If you try to do something that's not specified in the GraphQL schema, you'll get an error. Let's turn our REST interface into a GraphQL interface and see how it works.

# Create a simple GraphQL interface (screencast)

# Some cons of GraphQL (talking head)

- With GraphQL, sending a request to the server is a bit more complicated than with a REST interface, since you have to specify the query or mutation you want to make.

- GraphQL suffers from the n+1 problem. If you retrieve a bunch of blogs with authors, a separate database request will be made for each author, which potentially slows things down.

- The GraphQL language is verbose in some cases. For example, specifying a mutation is a pain. I think this should be shortened.

- Not everything in GraphQL is standardized. For example, it would be nice to have a standard way to do search and pagination (with page sizes and results, or using cursors). Also, having standard options for authentication, roles, and permissions, would be a great improvement.

# When to use REST vs GraphQL (talking head)

- First off, because REST interfaces are really simple to use, they're great for smaller applications, and for public-facing APIs. But really important: you have to be careful about security. Only expose data that you want to be public. So make sure you use some kind of layered architecture where you explicitly translate data into its public form.

- For more complex applications that are tightly integrated and need specific datasets, GraphQL is a great option. Your frontend is going to be much easier to manage, especially if you use a GraphQL client like Apollo that supports things like automatic caching of local data, subscribing to changes, and more.

# Outro

I hope this video has been helpful. Give it a thumbs up if you liked it. Consider subscribing to my channel if you want to learn more about software design and development. Thanks for watching, take care, and see you soon.

# Updating a blog (REST)

curl -X POST -H "Content-Type: application/json" \
 -d '{"title": "I like this blog" }' \
 http://127.0.0.1:5000/blogs/2

# Updating a blog (GraphQL)

Below is an example of a GraphQL mutation for updating a blog

```
mutation UpdateBlog($id: ID!, $payload: BlogPayload!) {
    update_blog(id: $id, payload: $payload) {
        id
        title
        content
    }
}

```

Variables:

{
"id":1,
"payload": {
"title":"Hello this is a blog"
}
}
