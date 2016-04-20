import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr(),
  rockface: DS.belongsTo('rockface'),
  type: DS.attr(),
  type_hr: DS.attr(),
  grade: DS.attr(),
  grade_hr: DS.attr(),
  short_description: DS.attr(),
  first_ascent_name: DS.attr(),
  first_ascent_year: DS.attr(),
  length: DS.attr(),
  nr_of_bolts: DS.attr()
});
