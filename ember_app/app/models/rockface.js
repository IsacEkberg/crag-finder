import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr(),
  no_routes: DS.attr(),
  area: DS.belongsTo('area'),
  routes: DS.hasMany('route'),
  image: DS.hasMany('rockfaceimage', {async: true}),
  geo_data: DS.attr(),
  short_description: DS.attr(),
  long_description: DS.attr()

});
