var map;
var markers = [];
var mlen = 0;
var which = 1;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lng: -122.26980401685347, lat: 37.86759094830563},
        zoom: 14
    });

    map.addListener("click", function(ev){
        var mtitle;
        if (which == 1) {
            mtitle = "Start";
        }
        else {
            mtitle = "End";
        }
        var m = new google.maps.Marker({
            position: ev.latLng,
            map: map,
            title: mtitle
        });

        if (markers.length < 2) {
            markers[markers.length] = m;
        }
        else {
            markers[which-1].setMap(null);
            markers[which-1] = m;
        }

        if (which == 1) {
            $("#p1x").val(ev.latLng.lng());
            $("#p1y").val(ev.latLng.lat());
            which = 2;
        }
        else {
            $("#p2x").val(ev.latLng.lng());
            $("#p2y").val(ev.latLng.lat());
            which = 1;
        }
            
        console.log(ev.latLng.lat());
        console.log(ev.latLng.lng());
    });
}

var poly = null;

$(document).ready(function(){
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
        data = {
            "start": {
                type: "coordinate",
                x: parseFloat($("#p1x").val()),
                y: parseFloat($("#p1y").val())},
            "end": {
                type: "coordinate",
                x: parseFloat($("#p2x").val()),
                y: parseFloat($("#p2y").val())}};
        xhr.send(JSON.stringify(data));
    });
});

