import DS from 'ember-data';

export default DS.Model.extend({
  image: DS.attr(),
  rockface: DS.belongsTo('rockface'),
  route_set: DS.hasMany('route')
});
