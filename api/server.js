const express = require('express');
const { ApolloServer } = require('apollo-server-express');
const Redis = require('ioredis');

const typeDefs = require('./schema')
const resolvers = require('./resolvers')

console.log(process.env.REDIS_MASTER_SERVICE_HOST);
console.log(process.env.REDIS_MASTER_SERVICE_PORT);

const redis = new Redis({host: process.env.REDIS_MASTER_SERVICE_HOST, port: process.env.REDIS_MASTER_SERVICE_PORT || 6379})
const app = express()

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: { redis }
})

server.applyMiddleware({ app })
app.listen({ port: 4000 }, () =>
  console.log(`🚀 Server ready at http://localhost:4000${server.graphqlPath}`)
)
