/**
 * Created by isac on 2016-06-10.
 */

/* globals $: true */
/* globals django: false */
/* globals fabric: false */

if(!$) {
    $ = django.jQuery;
}

function get_data(id) {
    var data_promise = $.Deferred();
    //Parallel: Rockface(then routes) & image(then nodes)

    function get_routes_data(routes) {
        var route_promise = $.Deferred();
        var route_data = {}; //Holds the data when finished.

        function get_route_data(route){ //Get a single route.
            return $.getJSON('/api/v1/routes/' + route).done(function (data) {
                route_data[route] = data;
            });
        }

        var promise_array = [];
        $.each( routes, function (index, route) {
            promise_array.push(get_route_data(route));
        });

        //When all promises in the promise_array are resolved. Resolve and return data.
        $.when.apply($, promise_array).done(function () {route_promise.resolve(route_data);});

        return route_promise;
    }

    function get_rockface_data(rockface_id){
        var rockface_promise = $.Deferred();
        var rockface_data = null;
            $.getJSON('/api/v1/rockfaces/' + rockface_id)
                .done(function ( data ) {
                    rockface_data = data;
                    return get_routes_data(rockface_data.routes)
                        .done(function (route_data) {
                            rockface_promise.resolve({
                                rockface: rockface_data, routes: route_data});
                        }
                    );
                });
        return rockface_promise;
    }

    function get_image_data(rockface_id){
        var image_promise = $.Deferred();
        $.getJSON('http://127.0.0.1:1337/api/v1/rockfaceimages/?rockface=' + id).
            done(function (rockfaceimage_data) {
            image_promise.resolve(rockfaceimage_data);
        });
        return image_promise;
    }


    $.when(get_rockface_data(id), get_image_data(id)).done(function (rockface_data, image_data) {
       data_promise.resolve({
           rockface: rockface_data.rockface,
           routes: rockface_data.routes,
           image: image_data[0]
       });
    });


    return data_promise;
    }

function insert_dom_elements(w, h, routes, route_callback) {
    var $canvas_element = "<canvas id=\"fabric_canvas\" width=\"" + w + "\" height=\"" + h + "\"></canvas>";
    var $route_list = $("<form>", {id: 'route-list'});

    var $target_element = $("div#content-main");
    $.each(routes, function (index, route) {
        var $element = $("<div>", {class: "route"});
        var $name = $("<p>").text(route.name);
        var $checkbox = $("<input>", {type:'radio', name: 'route-select', value: route.id});

        $checkbox.change(function() {
            //returns id of selected route to callback.
            route_callback($(this).val());
        });

        $element.append($checkbox);
        $element.append($name);
        $route_list.append($element);
    });



    $target_element.prepend($route_list);
    $target_element.prepend($canvas_element);


}


$('document').ready(function(){
    //Global variables:

    //Fabric canvas
    var canvas = null;

    //Fabric constants
    var CIRCLE_RADIUS = 12;
    var CIRCLE_THICKNESS = 5;
    var CIRCLE_ACTIVE_COLOR = '#006607';
    var CIRCLE_SELECTED_COLOR ='#00FF0B';
    var CIRCLE_INACTIVE_COLOR = '#666666';

    var LINE_THICKNESS = '5';
    var LINE_ACTIVE_COLOR = '#00A109';
    var LINE_INACTIVE_COLOR = '#666666';



    var TRANSPARENT_COLOR = 'rgba(0,0,0,0)';

    //Routes, nodes, client side variables.
    var selectedObject = null;  //Selected node.
    var routes = {};  //Holds properties of arrays (name=route_id). Circles are in array. Element 0 is first
    /*
       EXAMPLE:

        routes = {
            1: [circle_0, circle_1, circle_2],
            2: [circle_0, circle_3, circle_4, circle_5],
            3: [circle_6, circle_7, circle_5]
        }

        3 routes, route 1 & 2 share start. route 2 & 3 share end anchor.
        circle 0 & 6 are starting nodes.
     */

    var lines = {}; //Holds the drawn lines between route nodes.
    /*
        EXAMPLE:

        lines = {
            1: [line_0_1, line_1_2],
            2: [line_0_3, line_3_4, line_4_5],
            3: [line_6_7, line_7_5]
        }
        Based on routes example above. line_x_y refers to the line between node x and y.
        lines property (1-3 in example) are Django route IDs, same as in routes.
    */
    var active_route = null; //The selected route

    //Django ID of image.
    var object_id = false;

    function onCanvasClick(options){
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
        if(active_route == null) {
            alert("Välj en led först.");
            return;
        }
        console.log("addPoint()");
        var circle = new fabric.Circle({
            left: x - CIRCLE_RADIUS,
            top: y - CIRCLE_RADIUS,
            strokeWidth: CIRCLE_THICKNESS,
            radius: CIRCLE_RADIUS,
            fill: TRANSPARENT_COLOR,
            stroke: CIRCLE_ACTIVE_COLOR
        });
        circle.hasBorders = circle.hasControls = false;
        circle.on({
            'selected': markSelectedCircle
        });
        circle.selected = true;
        canvas.add(circle);
        routes[active_route].push(circle);
        drawLines();
    }

    function markSelectedCircle() {
        console.log('markCircle()');
        unMarkCircle(selectedObject);
        this.animate('radius', CIRCLE_RADIUS+3, {
            onChange: canvas.renderAll.bind(canvas),
            duration: 200
        });
        this.set('stroke', CIRCLE_SELECTED_COLOR);
        selectedObject = this;
        var in_route = false;
        var current_circle = this;  //What this refers to changes in each loop...
        $.each(routes[active_route], function (index, circle) {
            if(current_circle === circle){
                console.log("Marked circle already added to route");
                in_route = true;
            }
        });
        if(!in_route){
            console.log("Adding marked route to active route!");
            routes[active_route].push(this);  //add to the active route.
            drawLines();
        }
        console.log(routes);
    }

    function markActiveCircles() {
      console.log('markActiveCircles()');
      $.each(routes, function (index, route) {
          $.each(route, function (index, circle) {
                  circle.set('stroke', CIRCLE_INACTIVE_COLOR);
          });
      });
      $.each(routes[active_route], function (index, circle) {
              circle.set('stroke', CIRCLE_ACTIVE_COLOR);
      });
      canvas.renderAll();
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
      s.set('stroke', CIRCLE_ACTIVE_COLOR);
    }

    //Unselect the selected and switch route to edit.
    function activate_route_cb(route){
        active_route = route;
        unMarkCircle(selectedObject);
        selectedObject = null;
        markActiveCircles();
        console.log("Activated route: " + route);
    }

    function drawLines(){
        function makeLine() {
            var line = new fabric.Line({
               fill: LINE_ACTIVE_COLOR,
               stroke: LINE_ACTIVE_COLOR,
               strokeWidth: LINE_THICKNESS,
               selectable: false
            });
            line.set('fill', LINE_ACTIVE_COLOR);
            line.set('stroke', LINE_ACTIVE_COLOR);
            line.set('strokeWidth', 5);
            line.set('selectable', false);
            return line;
        }
        function setLineCoords(line, i, j){
            line.set('x1', i.left + CIRCLE_RADIUS);
            line.set('y1', i.top + CIRCLE_RADIUS);
            line.set('x2', j.left + CIRCLE_RADIUS);
            line.set('y2', j.top + CIRCLE_RADIUS);
        }

        console.log("Draw lines!");
        $.each(routes, function (route_id, route) {
            if(route.length > 1){
                for(var i = 1; i < (route.length); i++){

                    if(!(route_id in lines)){
                        lines[route_id] = [];
                    }

                    var line = null;
                    if(typeof lines[route_id][i-1] === 'undefined'){
                        line = makeLine();
                        setLineCoords(line, route[i-1], route[i]);
                        lines[route_id].push(line);
                        canvas.add(line);
                        line.sendToBack();
                        console.log("Added line:");
                    } else {
                        line = lines[route_id][i-1];
                        setLineCoords(line, route[i-1], route[i]);
                    }
               }
            } else {
                console.log("No line for route: " + route_id);
            }
        });
        console.log("RenderAll()");
        canvas.renderAll();
    }

    function init() {
        console.log("Fabric loaded.");
        console.log(object_id);
        get_data(object_id).done(function ( data ) {
            console.log("Loaded rockface+image data.");
            console.log(data);
            var w = data.image.image_width;
            var h = data.image.image_height;
            $.each(data.routes, function (index, route) {
                routes[route.id] = [];
            });
            insert_dom_elements(w, h, data.routes, activate_route_cb);
            canvas = new fabric.Canvas("fabric_canvas");
            canvas.setBackgroundImage(data.image.image, canvas.renderAll.bind(canvas), {
                backgroundImageStretch: false
            });
            canvas.selection = false; //Disables box selection
            canvas.on({
                'mouse:down': onCanvasClick,
                'object:moving': drawLines
            });
        });
    }

    //Start.
    object_id = $("div.field-rockface_key").children("div").children("p").text();
    if(object_id){
        $.getScript('https://cdnjs.cloudflare.com/ajax/libs/fabric.js/1.6.2/fabric.min.js', init);
    } else {
        console.log("No id found.");
    }
});


