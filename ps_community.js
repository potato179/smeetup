const mysql_con = require("./public/script/mysql_con.js");
var con = mysql_con.con;

function main(req, res, next){
    res.sendFile("main.html", {root: __dirname});
}

function writeitem_html(req, res, next){
    res.sendFile("writeitem.html", {root: __dirname});
}

function writeitem(req, res, next){
    var title = req.query.title;
    var writer = req.query.writer;
    var context = req.query.context;
    var fund_rate = req.query.fund_rate;
    var q = `insert into items (title, writer, context, fund_rate, state, comments, likes) values("${title}", "${writer}", "${context}", "${fund_rate}", "팀빌딩", {}, [])`;
    con.query(q, function(err, result){
        if(err) throw err;
        res.send({
            condition: "success",
            message: "정상적으로 등록되었습니다."
        });
    })
}

function view_group_html(req, res, next){
    res.sendFile("view_group.html", {root: __dirname});
}

function community_html(req, res, next){
    res.sendFile("community.html", {root: __dirname});
}

function view_community_html(req, res, next){
    res.sendFile("view_community.html", {root: __dirname});
}

function chat_html(req, res, next){
    res.sendFile("chat.html", {root: __dirname});
}

function view_chat_html(req, res, next){
    res.sendFile("view_chat.html", {root: __dirname});
}

function mypage_html(req, res, next){
    res.sendFile("mypage.html", {root: __dirname});
}

exports.main = main;
exports.writeitem_html = writeitem_html;
exports.writeitem = writeitem;
exports.view_group_html = view_group_html;
exports.community_html = community_html;
exports.view_community_html = view_community_html;
exports.chat_html = chat_html;
exports.view_chat_html = view_chat_html;
exports.mypage_html = mypage_html;