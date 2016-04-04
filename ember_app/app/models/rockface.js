import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr(),
  no_routes: DS.attr(),
  area: DS.belongsTo('area'),
  routes: DS.hasMany('route'),
  geo_data: DS.attr()
});
