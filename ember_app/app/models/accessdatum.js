/**
 * Created by jonathan on 2016-06-14.
 */
import DS from 'ember-data';

export default DS.Model.extend({
  short_message:DS.attr(),
  long_message: DS.attr(),
  start_date: DS.attr(),
  stop_date: DS.attr(),
  rock_face: DS.hasMany('rockface')
});
