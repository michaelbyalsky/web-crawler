db.createUser({
  user: "scrawler",
  pwd: "scrawlerpassword",
  roles: [{ role: "readWrite", db: "pastedb" }],
});
