$(function () {
    // setup autocomplete function pulling from currencies[] array
    $("#autocomplete").autocomplete({
        delay: 500,
        source: function (request, response) {
            $.getJSON("/action/query", {
                queryString: request.term,
                page_limit: 20
            }, function (data) {
                // data is an array of objects and must be transformed for autocomplete to use
                var array = data.data.length == 0 ? [] : $.map(data.data[0].fields, function (m) {
                    return {
                        label: m['value'],
                        url: null
                    };
                });
                response(array);
            });
        },
        focus: function (event, ui) {
            // prevent autocomplete from updating the textbox
            event.preventDefault();
        },
        select: function (event, ui) {
            // prevent autocomplete from updating the textbox
            event.preventDefault();
            // navigate to the selected item's url
            codeAddress(ui.item.label);
        }
    });

});
$(document).ready(function () {
    // your code here
});

var geocoder;
var map;
var drawingManager;
var placeIdArray = [];
var polylines = [];
var snappedCoordinates = [];
function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(-34.397, 150.644);
    var mapOptions = {
        zoom: 13,
        center: latlng
    }
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    // Try HTML5 geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);

            map.setCenter(pos);
        }, function () {
            handleNoGeolocation(true);
        });
    } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }
    runSnapToRoad();
}

function runSnapToRoad(path) {
    var pathValues = [];
    /*
     pathValues.push("1.3896777,103.987625536019");
     pathValues.push("1.3896777,103.9874997");
     pathValues.push("1.3895477,103.9870333");
     pathValues.push("1.3889236,103.9872226");
     pathValues.push("1.3886291,103.987312");
     pathValues.push("1.3882018,103.9873331");
     */
    $.get('/action/route', {}, function (data) {
            var dat= JSON.parse(data).data;
            for (var i = 0; i < dat.length; i++) {
                pathValues.push(''+dat[i].lat + ',' + dat[i].long);
                if(i==50)
                    break;
            }
            $.get('https://roads.googleapis.com/v1/snapToRoads', {
                interpolate: true,
                key: 'AIzaSyDRU6iqHkIqWN315IE4i7tmGIIurf3MtrU',
                path: pathValues.join('|')
            }, function (data) {
                console.log('Response for the server is ...' + data);
                processSnapToRoadResponse(data);
                drawSnappedPolyline();
            });
        }
    );


}
// Store snapped polyline returned by the snap-to-road method.
function processSnapToRoadResponse(data) {
    snappedCoordinates = [];
    placeIdArray = [];
    for (var i = 0; i < data.snappedPoints.length; i++) {
        var latlng = new google.maps.LatLng(
            data.snappedPoints[i].location.latitude,
            data.snappedPoints[i].location.longitude);
        snappedCoordinates.push(latlng);
        placeIdArray.push(data.snappedPoints[i].placeId);
    }
}
var apiKey = 'AIzaSyDRU6iqHkIqWN315IE4i7tmGIIurf3MtrU';

// Draws the snapped polyline (after processing snap-to-road response).
function drawSnappedPolyline() {
    var snappedPolyline = new google.maps.Polyline({
        path: snappedCoordinates,
        strokeColor: 'black',
        strokeWeight: 3
    });

    snappedPolyline.setMap(map);
    polylines.push(snappedPolyline);
}


function handleNoGeolocation(errorFlag) {
    if (errorFlag) {
        var content = 'Error: The Geolocation service failed.';
    } else {
        var content = 'Error: Your browser doesn\'t support geolocation.';
    }

    var options = {
        map: map,
        position: new google.maps.LatLng(60, 105),
        content: content
    };

    var infowindow = new google.maps.InfoWindow(options);
    map.setCenter(options.position);
}

function codeAddress(address) {
    //var address = document.getElementById('address').value;
    geocoder.geocode({'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                zoom: 10,
                position: results[0].geometry.location
            });
            // Construct the circle for each value in citymap.
            // Note: We scale the area of the circle based on the population.
            /*            var citymap = {};
             citymap['chicago'] = {
             center: new google.maps.LatLng(41.878113, -87.629798),
             population: 2714856
             };
             citymap['newyork'] = {
             center: new google.maps.LatLng(40.714352, -74.005973),
             population: 8405837
             };
             citymap['losangeles'] = {
             center: new google.maps.LatLng(34.052234, -118.243684),
             population: 3857799
             };
             citymap['vancouver'] = {
             center: new google.maps.LatLng(49.25, -123.1),
             population: 603502
             };*/

            var inner;
            var populationOptions = {
                strokeColor: '#00FF00',
                strokeOpacity: 0.8,
                strokeWeight: 3,
                fillColor: '#00FF00',
                fillOpacity: 0.35,
                map: map,
                center: results[0].geometry.location,
                radius: 1000
            };
            inner = new google.maps.Circle(populationOptions);

            var outer;
            var optionsOuter = {
                strokeColor: '#f6b6d6',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#f6b6d6',
                fillOpacity: 0.45,
                map: map,
                center: results[0].geometry.location,
                radius: 2000
            };
            outer = new google.maps.Circle(optionsOuter);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

google.maps.event.addDomListener(window, 'load', initialize);