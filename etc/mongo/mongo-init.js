// TODO: Need to look again at this file when implement authentication for MongoDB in docker-compose

db.createUser({
  user: process.env.MONGODB_USERNAME,
  pwd: process.env.MONGODB_PASSWORD,
  roles: [
    {
      role: "dbOwner",
      db: process.env.MONGODB_DATABASE,
    },
  ],
});
