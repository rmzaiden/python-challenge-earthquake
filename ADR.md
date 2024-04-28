| date       | writer                | status      |
| ---------- | --------------------- | ----------- |
|2024-04-20  |rodrigomz88@gmail.com  |Accepted     |

# ADR

## Context

We selected Python for the development of HTTP microservices due to its ease of development.

We considered the following frameworks for HTTP microservices development:
Python - FastAPI

### 1) Performance

- **FastAPI:** Highly performant due to its asynchronous nature and the use of Uvicorn, an ASGI server. Generally faster than traditional Python frameworks like Flask and Django.

#### 2) Ease of Use

- **FastAPI:** Considered easy to learn, especially for those with experience in Python. Its syntax is clear and straightforward, offering robust features with less code.

#### 3) Ideal Use Cases

- **FastAPI:** Excellent for high-performance APIs, especially when dealing with asynchronous operations. Ideal for applications requiring fast and efficient request processing.

#### 4) Scalability

- **FastAPI:** Its asynchronous nature makes it highly scalable, particularly suited for applications that may experience traffic spikes.

#### Conclusion

FastAPI is chosen for its performance and simplicity for REST APIs.

## Decision

> Python + FastAPI

Python is a language where most data handling demands and integrations with other systems can leverage the following positive points:

- (+) Most data professionals have experience with Python.
- (+) It has a mature and consolidated ecosystem of data handling libraries and system integration. This facilitates the throughput of demands, as there is no need to develop new libraries.
- (+) Python has a quicker learning curve than Java or C#, for example, which eases the entry of new professionals into the team.
- (+) The ability to process HTTP requests asynchronously (Async/Await), which allows for better performance and scalability.

## Consequences

The decision to proceed with Python + FastAPI does not block future implementation of microservices in other languages if this chosen framework proves inefficient for a particular demand.

Ultimately, this decision aims to make the development of microservices simpler, faster, and more efficient.