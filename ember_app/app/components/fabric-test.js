import Ember from 'ember';
  /* global fabric */
export default Ember.Component.extend({
  didInsertElement() {
    this._super(...arguments);
    var canvas = new fabric.Canvas("test_fabric");

    canvas.on({
      'mouse:down': onCanvasClick
    });

    var selectedObject = null;
    var routes = [];
    var line = null;

    //Size constants
    var CIRCLE_RADIUS = 12;
    var CIRCLE_THICKNESS = 5;

    function onCanvasClick(options) {
      console.log("onCanvasClick()");

      //Clicked a pre-existing point. Unmark previous + mark new.
      if(options.target != null){
        console.log("- Pre-existing point. Unmark(old)+mark(new)");
      }

      //Nothing clicked. New or connect point.
      else if(options.target == null){
        console.log("- New point");
        addPoint(options.e.offsetX, options.e.offsetY);
      }
    }

    function addPoint(x, y){
      console.log("addPoint()");
      var circle = new fabric.Circle({
          left: x - CIRCLE_RADIUS,
          top: y - CIRCLE_RADIUS,
          strokeWidth: CIRCLE_THICKNESS,
          radius: CIRCLE_RADIUS, //To mark it....
          fill: '#fff',
          stroke: '#666'
      });
      circle.hasBorders = circle.hasControls = true;
      circle.on({
        'selected': markCircle
      });
      canvas.add(circle);
      routes.push(circle);
    }

    function markCircle() {
      console.log('markCircle()');
      unMarkCircle(selectedObject);
      this.animate('radius', CIRCLE_RADIUS+3, {
        onChange: canvas.renderAll.bind(canvas),
        duration: 200
      });
      selectedObject = this;
    }

    function unMarkCircle(s) {
      console.log('unMarkCircle()');
      if (s == null) {
        console.log("- null");
        return;
      }
      s.animate('radius', CIRCLE_RADIUS, {
        onChange: canvas.renderAll.bind(canvas),
        duration: 200
      });
    }

    function renderLine(){

      if (routes.length > 1){
        var sx = routes[0].x;
        var sy = routes[0].y;
      }
    }

  }
});
