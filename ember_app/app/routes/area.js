import Ember from 'ember';

export default Ember.Route.extend({
  activate() {
    window.scrollTo(0,0);
  },
  model(params) {
    return this.store.findRecord('area', params.id);
  }
});
