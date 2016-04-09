import Ember from 'ember';
/* globals DS */
/* globals $ */
export default Ember.Component.extend({
  area: null,
  gmapsService: Ember.inject.service('gmaps-service'),
  new_map_service: DS.PromiseObject(),
  map: null,
  mapOptions: function () {
    return {
      center: {lat: 60.662, lng: 15.681},
      zoom: 6
    };
  },

  didInsertElement() {
    function parse_geo_data(s) {
      if(!s){
        console.log("No previous data");
        return;
      }
      var arr = s.split(";");
      var arr2 = [];
      $.each(arr,function( index, value2 ) {
        if(value === "") {return;}
        var value = value2.substring(1, value2.length-1);
        var vals2 = value.split(", ");
        if(vals2 === "") {return;}
        arr2.push({lat:parseFloat(vals2[0]), lng:parseFloat(vals2[1])});
      });
      console.log(arr2);
      return arr2;
    }

    this._super(...arguments);
    var area = this.get('area');

    //This loads the google maps script using a ember service.
    this.get('gmapsService').loadScript().then(function () {
      /* globals google */
      console.log("Initiating gmaps");
      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 6,
        center: {lat: 60.662, lng: 15.681}
      });

      //This loads all the rockfaces and places poly lines:
      var rockfaceRef = area.get('rockfaces');
      rockfaceRef.then((rockfaces) => {

        //This bound box is used to calculate the center of the points in this area.
        var bound = new google.maps.LatLngBounds();

        rockfaces.forEach(function (value) {
          var marker_array = parse_geo_data(value.get('geo_data'));
          console.log(marker_array);

          //Create a polyline from each marker point.
          var poly = new google.maps.Polyline({
            path: marker_array,
            strokeColor: '#000000',
            strokeOpacity: 1.0,
            strokeWeight: 3,
            editable: false
          });
          poly.setMap(map);

          //add points to boundbox.
          marker_array.forEach(function (el) {
            bound.extend(new google.maps.LatLng(el));
          });

        });
        //TODO: Save/calculate zoom level. In django model?
        map.setCenter(bound.getCenter());
      });

    });
  }
});
