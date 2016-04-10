import Ember from 'ember';
var $ = Ember.$;

export default Ember.Component.extend({
  filter: null,

  showAutoComplete: Ember.computed('inputFocused', 'autoCompleteMenuFocused', function () {
    var input = this.get('inputFocused');
    //var menu = this.get('autoCompleteMenuFocused');
    return (input);
  }),

  dropdownClass: Ember.computed('showAutoComplete', function () {
    if( this.get('showAutoComplete') ) {
      return 'open';
    } else {
      return '';
    }
  }),
  filteredList: null,
  inputFocused: false,
  autoCompleteMenuFocused: false,

  moveFocusDown: function () {
    console.log("Moving on.");
    $('.dropdown-menu').children().first().children().focus();
  },

  actions: {
    autoComplete(param, e) {
      var self = this;
      //if(e.keyCode === 40){
      //  console.log("Should move...");
      //  self.get('moveFocusDown')();
      //}
      self.get('autoComplete')(this.get('filter'));
    },
    focusIn() {
      this.set('inputFocused', true);
    },
    menuFocusIn() {
      console.log(($(".dropdown").children(".focus").length === 0));
      console.log("2!");
      this.set('autoCompleteMenuFocused', true);
    },
    focusOut() {
      this.set('inputFocused', false);
    }
  }

});
