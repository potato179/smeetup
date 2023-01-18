const http = require("http");
const express = require("express");
const app = express();
const mysqlconfig = require("./public/script/mysql_con.js");
const con = mysqlconfig.con;

const hostname = "127.0.0.1";
const port = "8001";

const ps_users = require("./ps_users.js");
const ps_community = require("./ps_community.js");
const urls = [
    {url: "/login", ps: ps_users.login},
    {url: "/login.html", ps: ps_users.login_html},
    {url: "/logout", ps: ps_users.logout},
    {url: "/join", ps: ps_users.join},
    {url: "/join.html", ps: ps_users.join_html},
    {url: "/main", ps: ps_community.main},
    {url: "/writeitem.html", ps: ps_community.writeitem_html},
    {url: "/view_group.html", ps: ps_community.view_group_html},
    {url: "/community.html", ps: ps_community.community_html},
    {url: "/view_community.html", ps: ps_community.view_community_html},
    {url: "/chat.html", ps: ps_community.chat_html},
    {url: "/view_chat.html", ps: ps_community.view_chat_html},
    {url: "/mypage.html", ps: ps_community.mypage_html}
];

process.argv.forEach(function(item, index) {
    if(item == "--port") port = Number(process.argv[index + 1]);
});

app.use("/public", express.static("public"));

app.get("/", function(req, res, next){
    res.sendfile("login.html", {root: __dirname});
});

urls.forEach(function(element, index){
    app.get(element.url, element.ps);
});

app.listen(port, () => {
    console.log(port, hostname);
});