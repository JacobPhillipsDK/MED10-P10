api_token = "pk.eyJ1IjoiamFjb2JwaGlsbGlwc2RrIiwiYSI6ImNsNGc5a2htNDAxbnAzY3M3OTBsbnB2anMifQ.4QOcID_maHtm87qYW_oqHw"


mapboxgl.accessToken = api_token;


const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/jacobphillipsdk/cltxdr8u300e801qsg909ckgn/draft', // style URL
  center: [9.9287, 57.0479], // starting position [lng, lat]
  zoom: 17, // starting zoo
});


// Add zoom and rotation controls to the map.
map.addControl(new mapboxgl.NavigationControl());






map.on('load', function() {
  map.addSource('single_point', {
    type: 'geojson',
    data: '../MED10-MAP/geodata/output.geojson' // Replace with the path to your local GeoJSON file
  });

  // Add a layer to render the point
  map.addLayer({
    id: 'Point',
    type: 'circle',
    source: 'single_point',
    paint: {
      'circle-radius': 6,
      'circle-color': 'red'
    }
  });
});

