# homomorphic-enc-and-search-system

## About project

System for encrypting data and searching for it (on full occurrence, for now)

## Implementation

- It uses for now a Paillier cryptosystem as an engine for homomorphic encr.
Paillier cryptosystem is a PARTICALLY HE, so it should be replaced on 
one of realisation of FULL HE.
- Project uses Postgres database to store enc user data.
- On the current stage project doesn't have any server

## Concepts of work

"Docs" -- is an abstraction of some data that user can store and find for it.
Docs (stored in Postgres db) have title and content. Both fields are encrypted
on the client side and sent to the server side, where store encrypted (ofc)

If user want to get access to its doc, it should find it via the title, so:
- Client will encrypt this one and send it to the server
- Server will find a difference, after what it send it to client
- Client to decode the difference. 
- If diff is equal zero, that this document is the one that the client 
was looking for: client send server a request on this doc.

## FOR NOW CLIENT AND SERVER IS WHOLE ONE

