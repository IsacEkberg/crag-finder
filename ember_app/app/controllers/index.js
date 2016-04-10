import Ember from 'ember';

export default Ember.Controller.extend({
  filteredList: null,
  actions: {
    autoComplete(param) {
      if(param !== "") {
        this.store.query('area', {search: param}).then((result) => {
          this.set('model',result);
        });
      } else {
        this.set('model', null);
      }
    },
    search(param) {
      if(param !== "") {
        this.store.query('area', {name: param}).then((result) => {
          this.set('model',result);
        });
      } else {
        this.set('model').clear();
      }
    }
  }
});
