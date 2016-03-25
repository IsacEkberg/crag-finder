import Ember from 'ember';

export default Ember.Component.extend({
  page_array: ['contact', 'about'],
  pages: {
    contact:{verbose: "Contact", route:"contact", status:false},
    about:{verbose: "About", route:"about", status:false}
  },
  activePage: "index",
  actions: {
    setActivePage(page) {
      this.activePage = page;
    }
  }
});
