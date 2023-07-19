- Langchain is a great library for creating applications that communicate with Large Language Model APIs.
- And you did mention in a survey I recently posted that you wanted me to do more AI-focused content.
- I do my best to listen to you. So here you go - I’ll show you what you can do with langchain and it’s pretty cool.
- But, I wouldn’t be Arjan if I didn’t also talk about how it’s designed. And we can learn an important lesson from that.

## Langchain tutorial

- Show basic setup of creating an LLM
- Show templating basics
- Show how to use the output parser with Pydantic to get JSON data
- Show the other way around: call an API via text
- What are the kinds of things you’d like to do with langchain in your own projects? Do you think any important features are currently missing? Let me know in the comments!

## About langchain’s design

- One strong point of langchain is that it defines common concepts such as prompts, language models and output parsers
- For each of these things, there’s a hierarchy of more specific implementations
  - For prompts there are human and system messages
  - For language models, there are implementations of several LLMs and Chat Models
  - For output parsers, you have a variety of different parser types, from lists, to JSON data, to datetime parsing and more.
- langchain combines elements from various design patterns:
  - Strategy (to select the LLM that you’d like to use)
  - Bridge (different LLMs work with different output parsers and you can add more LLMs and output parser independently because they’re coupled on the abstract level
  - Template Method (we provide the LLM instance and langchain call methods on it, including retries etc.
- What we can see with langchain is how important it is to software design to define the concepts well. If the concepts are wrong, your design is not going to work well.

## Final Thoughts

- What lesson can we learn from langchain’s design? You don’t need to implement design patterns strictly to get their benefit.
- So when you design a piece of software, don’t start with thinking about how you can apply a specific design pattern.
- Instead, depending on the language you use and the features that it offers, you can create something even better than the original design pattern.
- In the end, it’s all about the principles behind the patterns. As long as you follow those, you’ll write great code that goes beyond the patterns.
- One example of a set of principles is GRASP. Especially if you work a lot with Python, this is a great starting point. To learn more about it, watch this video next.
- Thanks for watching - see you next time!
