import DS from 'ember-data';

export default DS.Model.extend({
  image: DS.attr(),
  area: DS.belongsTo('area')
});
