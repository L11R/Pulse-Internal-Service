/*Jsgrid Init*/
$(function() {
	"use strict";

    $("#jsgrid_1").jsGrid({
        height: "450px",
        width: "100%",

        filtering: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 15,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete the client?",

        controller: db,

        fields: [
            { name: "order_id", title: "Номер заявки", type: "text", width: 150 },
            { name: "barcodes", title: "Баркод", type: "text", width: 150 },
            { name: "terminal", title: "Терминал", type: "text", width: 150 },
            { name: "point_settlement", title: "Город", type: "text", width: 150 },
            { name: "point_address", title: "Адрес", type: "text", width: 150 },
            { name: "sender", title: "Контрагент", type: "text", width: 150 },
            { name: "consignor", title: "Отправитель", type: "text", width: 150 },
            { name: "phone", title: "Телефон", type: "text", width: 150 },
            { name: "date_added", title: "Дата создания", type: "text", width: 150 },
            { name: "delivery_date", title: "Дата доставки", type: "text", width: 150 },
            { name: "upload_date", title: "Дата получения", type: "text", width: 150 },
            { name: "cod", title: "Наложка", type: "text", width: 150 },
            { name: "partner_service_fee", title: "Цена партнёра", type: "text", width: 150 },
            { name: "declared_price", title: "Объявленная ценность", type: "text", width: 150 },
            { name: "status", title: "Статус", type: "text", width: 150 },
            { type: "control" }
            //{ name: "Age", type: "number", width: 50 },
            //{ name: "Address", type: "text", width: 200 },
            //{ name: "Country", type: "select", items: db.countries, valueField: "Id", textField: "Name" },
            //{ name: "Married", type: "checkbox", title: "Is Married", sorting: false}

        ]
    });

});