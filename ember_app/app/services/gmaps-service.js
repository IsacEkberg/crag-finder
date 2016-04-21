import Ember from 'ember';

export default Ember.Service.extend({

  g:null,
  loading: false,
  getScript: function () {
    console.log("gmaps-service: ---Start of getScript---");
    var self = this;
    var loading = this.get('gmaps-service: loading');
    function set_g(g) {
      console.log("gmaps-service: Setting g to new script");
      self.set('g', g);
    }
    var g = this.get('g');

    if(loading){
      console.log("gmaps-service: Already loading script!");
      return;
    }

    return new Promise(function (resolve, reject) {
      if (g == null){
        console.log("gmaps-service: Gmaps not loaded, getting API...");

        Ember.$.ajax({
        //TODO: Extract API-key
          url: "https://maps.googleapis.com/maps/api/js?v=3.23&key=AIzaSyD3sdImCNCvjYXzqlePVqJ8u08alKCVKs0",
          dataType: 'script',
          cache: true
        }).done(() => {
          /* globals google */
          console.log("gmaps-service: Loaded API");
          set_g(google);
          console.log("gmaps-service: Got it!");
          resolve(google);
        });
      }
      else {
        console.log("gmaps-service: Gmaps loaded in service, sending google obj.");
        set_g(g);
        resolve(g);
      }
    });

  }

});
