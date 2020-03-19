var mymap = L.map('mapid').setView([51.505, -0.09], 13);
var twitterIcon = L.icon({iconUrl:'https://cdn2.iconfinder.com/data/icons/minimalism/128/twitter.png', iconSize: [64, 64]});
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
		'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox/streets-v11',
	tileSize: 512,
	zoomOffset: -1
}).addTo(mymap);
var layerGroup = L.layerGroup().addTo(mymap);

function showResultOnMap(result) {
	layerGroup.clearLayers();
	if (!$.isEmptyObject(result)) {
		let minLat = 90, maxLat = -90, minLng = 180, maxLng = -180;
		$.each(result, (idx, point) => {
			console.log(point);
			if (point.geo != null) {
				console.log(point.geo.coordinates);
				L.marker(point.geo.coordinates, {icon: twitterIcon}).addTo(layerGroup)
					.bindPopup(point.text);
				minLng = Math.min(minLng, point.geo.coordinates[0]);
				maxLng = Math.max(maxLng, point.geo.coordinates[0]);
				minLat = Math.min(minLat, point.geo.coordinates[1]);
				maxLat = Math.max(maxLat, point.geo.coordinates[1]);
				//mymap.setView([(minLng+maxLng)/2, (minLat+maxLat)/2], 5);
				mymap.setZoom(1);
			}
		});
	}
}

function searchHadoopBasic(query_str) {
	$.ajax({
		url: '/api/hadoop/?query=' + query_str,
		type: 'GET',
		success: function(data) {
			console.log(data['result']);
			showResultOnMap(data['result']);
		}
	});
}
