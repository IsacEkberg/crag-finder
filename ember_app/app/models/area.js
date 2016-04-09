import DS from 'ember-data';
import Ember from 'ember';

export default DS.Model.extend({
  name: DS.attr(),
  rockfaces: DS.hasMany('rockface', {async: true}),
  short_description: DS.attr(),
  long_description: DS.attr(),
  road_description: DS.attr(),
  severalRockfaces: Ember.computed('rockfaces.@each.[]', function () {
    return this.get('rockfaces').get('length') !== 1;
  })
});
