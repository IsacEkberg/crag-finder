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
    var ACTIVE_COLOR = 'rgba(255,0,0,1)';  //Red
    var SELECTED_COLOR = 'rgba(0,255,0,1)'; //Green
    var INACTIVE_COLOR = 'rgba(0,0,255,1)'; //Yellow
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
            stroke: ACTIVE_COLOR
        });
        circle.hasBorders = circle.hasControls = false;
        circle.on({
            'selected': markSelectedCircle
        });
        circle.selected = true;
        canvas.add(circle);
        routes[active_route].push(circle);
    }

    function markSelectedCircle() {
        console.log('markCircle()');
        unMarkCircle(selectedObject);
        this.animate('radius', CIRCLE_RADIUS+3, {
            onChange: canvas.renderAll.bind(canvas),
            duration: 200
        });
        this.set('stroke', SELECTED_COLOR);
        selectedObject = this;
        var in_route = false;
        $.each(routes[active_route], function (index, circle) {
            if(Object.is(this, circle)){
                console.log("Marked circle already added to route");
                in_route = true;
            }
        });
        if(!in_route){
            console.log("Adding marked route to active route!");
            routes[active_route].push(this);  //add to the active route.
        }
        console.log(routes);
    }

    function markActiveCircles() {
      console.log('markActiveCircles()');
      $.each(routes, function (index, route) {
          $.each(route, function (index, circle) {
                  circle.set('stroke', INACTIVE_COLOR);
          });
      });
      $.each(routes[active_route], function (index, circle) {
              circle.set('stroke', ACTIVE_COLOR);
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
      s.set('stroke', ACTIVE_COLOR);
    }

    //Unselect the selected and switch route to edit.
    function activate_route_cb(route){
        active_route = route;
        unMarkCircle(selectedObject);
        selectedObject = null;
        markActiveCircles();
        console.log("Activated route: " + route);
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
            canvas.on({
                'mouse:down': onCanvasClick
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


