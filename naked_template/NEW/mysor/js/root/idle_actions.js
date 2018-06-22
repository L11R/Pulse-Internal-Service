
document.getElementById("start_receive").onclick=function (e) {
    perform_post("/", { "action": "start_work", "preferred_mode": "receive" });
};

document.getElementById("start_insert").onclick=function (e) {
    perform_post("/", { "action": "start_work", "preferred_mode": "deliver" });
};
