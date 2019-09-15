var map;

var start_marker = null;
var end_marker = null;

var which = 1;

var start_point_x;
var start_point_y;
var end_point_x;
var end_point_y;

var start_pa = 1;
var end_pa = 1;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lng: -122.26980401685347, lat: 37.86759094830563},
        zoom: 14
    });

    map.addListener("click", function(ev){
        var m = new google.maps.Marker({
            position: ev.latLng,
            map: map,
            title: "REEE"
        });

        var block = false;
        if (start_pa == 1) {
            if (which == 1 || end_pa == 2) {
                console.log("start block");
                if (start_marker) {
                    start_marker.setMap(null);
                }
                m.setTitle("Start");
                start_marker = m;
                start_point_x = ev.latLng.lng();
                start_point_y = ev.latLng.lat();
                which = 2;
                block = true;
            }
        }
        if (end_pa == 1 && !block) {
            if (which == 2 || start_pa == 2) {
                console.log("end block");
                if (end_marker) {
                    end_marker.setMap(null);
                }
                m.setTitle("End");
                end_marker = m;
                end_point_x = ev.latLng.lng();
                end_point_y = ev.latLng.lat();
                which = 1;
            }
        }
            
        console.log(ev.latLng.lat());
        console.log(ev.latLng.lng());
    });
}

var poly = null;

$(document).ready(function(){
    $("#sSP").click(function(){
        start_pa = 1;
        $("#addr0").val("");
    });
    $("#sSA").click(function(){
        start_pa = 2;
        if (start_marker) {
            start_marker.setMap(null);
        }
    });
    $("#sEP").click(function(){
        end_pa = 1;
        $("#addr1").val("");
    });
    $("#sEA").click(function(){
        end_pa = 2;
        if (end_marker) {
            end_marker.setMap(null);
        }
    });

    $("#run").click(function(){
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/route", true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onload = function(){
            var data = JSON.parse(xhr.responseText);
            console.log(data);

            var path = [];
            var i;
            var clist = data["path"]["coords"];
            console.log(clist);
            for (i = 0; i < clist.length; i++) {
                path[path.length] = {
                    lng: parseFloat(clist[i][0]),
                    lat: parseFloat(clist[i][1])};
            }

            if (poly) {
                poly.setMap(null);
            }
            poly = new google.maps.Polyline({
                path: path,
                geodesic: true,
                strokeColor: "#FF0000",
                strokeOpacity: 1.0,
                strokeWeight: 2
            });
            poly.setMap(map);

        };

        var start_data;
        if (start_pa == 1) {
            start_data = {
                type: "coordinate",
                x: start_point_x,
                y: start_point_y};
        }
        else {
            start_data ={
                type: "address",
                address: $("#addr0").val()};
        }

        var end_data;
        if (end_pa == 1) {
            end_data = {
                type: "coordinate",
                x: end_point_x,
                y: end_point_y};
        }
        else {
            end_data = {
                type: "address",
                address: $("#addr1").val()};
        }

        data = {
            start: start_data,
            end: end_data};
        xhr.send(JSON.stringify(data));
    });
});

