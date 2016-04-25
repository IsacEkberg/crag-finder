import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('about');
  this.route('contact');
  this.route('area', { path: 'area/:id' });
  this.route('rockface', {path: 'rockface/:id'});
  this.route('construction');
  this.route('map');
  this.route('account');
});

export default Router;
