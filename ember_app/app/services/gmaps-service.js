import Ember from 'ember';

export default Ember.Service.extend({

  //TODO: Extract API-key
  loadScript: function (cb) {
    return new Promise(function (resolve, reject) {
      console.log("Getting script!");
      console.log(cb);
      Ember.$.ajax({
        url: "https://maps.googleapis.com/maps/api/js?key=AIzaSyD3sdImCNCvjYXzqlePVqJ8u08alKCVKs0",
        dataType: 'script',
        cache: true
      }).done(resolve).fail(reject);
    });
  }


});
