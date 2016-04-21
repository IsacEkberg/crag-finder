import Ember from 'ember';

export default Ember.Component.extend({
  currentTabName: null,
  findTabActive: Ember.computed('currentTabName', function () {
    var currentTabName = this.get('currentTabName');
    console.log(currentTabName === 'find');
    return currentTabName === 'find';
  }),
  actions: {
    setTabName: function (name) {
      this.set('currentTabName', name);
    }
  }
});
