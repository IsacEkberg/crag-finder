import Ember from 'ember';
/* globals $ */
export default Ember.Component.extend({
  area: null,
  map: null,
  renderOnInsert: false,  // If set to true is the component rendered direct.
  findTabActive: null,
  renderListener: Ember.observer('findTabActive', function () {
    console.log("renderListener - tripped");
    if(this.get('findTabActive')){
      console.log("renderListener - executing");
      this.renderMap();
      return true;
    }
    return false;
  }),
  gmapsService: Ember.inject.service('gmaps-service'),

  didInsertElement() {
    console.log("renderListener - didInsertElement");
    this._super(...arguments);
    if (this.get('renderOnInsert')){
      this.renderMap();
    }
    //TODO. Move some logic here to speed up tab switch?
  },
  //action: {
  renderMap() {
    console.log("gmaps-component - renderMap()");
    function parse_geo_data(s) {
      if(!s){
        console.log("No previous data");
        return;
      }
      var arr = s.split(";");
      var arr2 = [];
      $.each(arr,function( index, value2 ) {
        var value = value2.substring(1, value2.length-1);
        if(value === "") {return;}
        var vals2 = value.split(", ");
        if(vals2 === "") {return;}
        arr2.push({lat:parseFloat(vals2[0]), lng:parseFloat(vals2[1])});
      });
      console.log(arr2);
      return arr2;
    }
    var area = this.get('area');
    var map = this.get('map');

    //This loads the google maps script using a ember service.
    this.get('gmapsService').getScript().then(function (google) {
      console.log("google-maps comp: Initiating gmaps");
      console.log(google);

      map = new google.maps.Map(document.getElementById('map'), {
        zoom: 6,
        center: {lat: 60.662, lng: 15.681}
      });

      //This loads all the rockfaces and places poly lines:
      var rockfaceRef = area.get('rockfaces');
      console.log("google-maps comp: Loading rockfaces...");
      rockfaceRef.then((rockfaces) => {
        console.log("google-maps comp: Done loading rockfaces.");
        //This bound box is used to calculate the center of the points in this area.
        var bound = new google.maps.LatLngBounds();
        console.log("google-maps comp: bound-box:");
        console.log(bound);
        rockfaces.forEach(function (value) {
          var marker_array = parse_geo_data(value.get('geo_data'));
          console.log("google-maps comp: marker_array:");
          console.log(marker_array);

          //Create a polyline from each marker point.
          var poly = new google.maps.Polyline({
            path: marker_array,
            strokeColor: '#000000',
            strokeOpacity: 1.0,
            strokeWeight: 3,
            editable: false
          });
          console.log("google-maps comp: Poly line:");
          console.log(poly);
          poly.setMap(map);

          //add points to boundbox.
          marker_array.forEach(function (el) {
            var e = new google.maps.LatLng(el);
            if(!bound.contains(e)){
              bound.extend(e);
            }
          });

        });
        //TODO: Save/calculate zoom level. In django model?
        console.log("google-maps comp: Setting bound box:");
        google.maps.event.trigger(map, 'resize');
        map.fitBounds(bound);
        //this.set('map', map);
      });
    });
  }
  //}
});
