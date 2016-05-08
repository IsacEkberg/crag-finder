import Ember from 'ember';
  /* global fabric */
export default Ember.Component.extend({
  didInsertElement() {
    this._super(...arguments);
    var canvas = new fabric.Canvas("test_fabric");
    var rect = new fabric.Rect({
      left: 100,
      top: 100,
      fill: 'red',
      width: 20,
      height: 20
    });
    canvas.add(rect);
  }
});
