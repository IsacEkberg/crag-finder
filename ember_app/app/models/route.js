import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr(),
  rockface: DS.belongsTo('rockface'),
  type: DS.attr(),
  grade: DS.attr()
});
