import Ember from 'ember';
var $ = Ember.$;

export default Ember.Component.extend({
  filter: null,
  dropdownClass: Ember.computed('focused', function () {
    if( this.get('focused') ) {
      return 'open';
    } else {
      return '';
    }
  }),
  filteredList: null,
  focused: false,

  moveFocusDown: function () {
    console.log("Moving on.");
    $('.dropdown-menu').children().first().children().focus();
  },

  actions: {
    autoComplete(param, e) {
      var self = this;
      if(e.keyCode === 40){
        console.log("Should move...");
        self.get('moveFocusDown')();
      }
      self.get('autoComplete')(this.get('filter'));
    },
    focus() {
      this.set('focused', true);
    }
  }
});
