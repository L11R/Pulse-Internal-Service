/*Jsgrid Init*/
$(function() {
	"use strict";

    $("#jsgrid_1").jsGrid({
        height: "450px",
        width: "100%",

        filtering: true,
        editing: false,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 15,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete the client?",

        controller: db,

        fields: [
            { name: "order_id", title: "Номер заявки", type: "text", width: 150 }


        ]
    });

});