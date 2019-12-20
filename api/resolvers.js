module.exports = {
  Query: {
    listUnits: async(parent, {}, {redis}) => {
        try {
          return await redis.lrange("available_units", 0, -1)
        } catch(error) {
          return null
        }
    },
    unitHistory: async(parent, {id}, {redis}) => {
        try {
            const response = await redis.zrevrange("vehicle_id:"+id, 0, -1)
            return response.map(unit => JSON.parse(unit.replace(/'/g, "\"")) )
        } catch(error) {
            console.log(error)
            return null
        }
    },
    listAlcaldias: async(parent, {}, {redis}) => {
      try {
        return await redis.smembers("available_alcaldias")
      } catch(error) {
        console.log(error)
        return null
      }
    },
    unitsbyAlcaldia: async(parent, {alcaldia}, {redis}) => {
      try {
        return await redis.hkeys("alcaldia:"+alcaldia)
      } catch(error) {
        console.log(error)
        return null
      }
    }
  }
}
