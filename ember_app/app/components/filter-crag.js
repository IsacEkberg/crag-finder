import Ember from 'ember';

export default Ember.Component.extend({
  areas: null,
  names: Ember.computed('areas', function () {
    var data = this.get('areas');
    var nameArray = [];
    data.forEach(function (element) {
      nameArray.push(element.get('name'));
    });
    return nameArray;
  }),
  didInsertElement() {
    console.log("adding data");
    var names = this.get('names');
    var data = this.get('areas');
    var wantedArea = this.get('wantedArea');
    Ember.$("#area-search").autocomplete({
      source: names,
      //position: { my : "left top", at: "left top" },
      appendTo: Ember.$("#search-results"),
      select: function (event, ui) {
        var target = ui.item.value;
        var targetModel = null;
        data.forEach(function (element) {
          if (element.get("name") === target){
            targetModel = element;
          }
          if (targetModel === null) {
            console.error("Got null as target model to transition to");
          } else {
            console.log("Transition!");
            wantedArea(targetModel);
          }

        });

      }
    });
  },
  willDestroyElement() {
    Ember.$("#area-search").autocomplete( "destroy" );
  }
});
