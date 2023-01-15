const mysql = require("mysql");
const token = require("./mysql_token.json")

const con = mysql.createConnection({
    host: token.host,
    user: token.user,
    password: token.password,
    database: token.database
});

con.connect(function(err) {
    if (err) throw err;
});

exports.con = con; 