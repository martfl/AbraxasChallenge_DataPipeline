const { gql } = require('apollo-server-express');
module.exports = gql`
  type Unit {
    coords: [String],
    alcaldia: String!,
    date_updated: String
  }

  type Query {
    listUnits: [Int]!,
    unitHistory(id: Int!): [Unit],
    listAlcaldias: [String]!,
    unitsbyAlcaldia(alcaldia: String!): [String]!
  }
`

