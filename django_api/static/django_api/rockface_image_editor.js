/**
 * Created by isac on 2016-06-10.
 */

/* globals $: true */
/* globals django: false */
/* globals fabric: false */
function print(input){console.log(input)}
if(!$) {
    $ = django.jQuery;
}
$('document').ready(function(){
    //Global variables:
    var SAVE_ROUTE_NODE_URL = '/api/v1/routenodes/save/';

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
    var rockface_id = false;
    var rockfaceimage_id = false;

    var history = [];

    function get_data(id) {
        var data_promise = $.Deferred();
        //Parallel: Rock face (then routes) & image(then nodes)

        function get_routes_data(routes) {
            var route_promise = $.Deferred();
            var route_data = {}; //Holds the data when finished.
            var old_nodes = null;
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
            $.getJSON('/api/v1/rockfaceimages/?rockface=' + id).
            done(function (rockfaceimage_data) {
                image_promise.resolve(rockfaceimage_data);
            });
            return image_promise;
        }
        function get_old_nodes(){
            var old_node_promise = $.Deferred();
            $.get("/api/v1/routenodes/?image=" + rockfaceimage_id).done(function (data) {
                old_node_promise.resolve(data);
            });
            return old_node_promise;
        }

        $.when(get_rockface_data(id), get_image_data(id), get_old_nodes()).done(function (rockface_data, image_data, old_nodes) {
            data_promise.resolve({
                rockface: rockface_data.rockface,
                routes: rockface_data.routes,
                image: image_data[0],
                old_nodes: old_nodes
            });
        });


        return data_promise;
    }

    function insert_dom_elements(w, h, routes, route_callback, save_callback, undo_callback) {
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

        var $save_button = $("<input>", {type: 'submit', class: 'default', value: 'Spara'});
        $save_button.click(function (e) {
            // console.log("Save button clicked.");
            e.preventDefault();
            save_callback();
        });
        var $undo_button = $("<input>", {type: 'submit', class: 'default', value: 'Ångra'});
        $undo_button.click(function (e) {
            // console.log("Undo button clicked.");
            e.preventDefault();
            undo_callback();
        });

        $target_element.prepend($route_list);
        $target_element.prepend($undo_button);
        $target_element.prepend($save_button);
        $target_element.prepend($canvas_element);


    }



    function onCanvasClick(options){
        // console.log("onCanvasClick()");
        //Clicked a pre-existing point. Unmark previous + mark new.
        if(options.target != null){
            // console.log("- Pre-existing point. Unmark(old)+mark(new)");
        }

        //Nothing clicked. New or connect point.
        else if(options.target == null){
            // console.log("- New point");
            circle = addPoint(options.e.offsetX, options.e.offsetY);
            circle.lockMovementX = false;
            circle.lockMovementY = false;
        }
    }

    function addPoint(x, y, force_route = false){
        var offset = CIRCLE_RADIUS;
        if(active_route == null && force_route === false) {
            alert("Välj en led först.");
            return;
        } else if(force_route){
            // console.log("Force insert point.");
            offset = 0;  // If force is it the true top/left values being sent.
        }
        // console.log("addPoint()");
        var circle = new fabric.Circle({
            left: x - offset,
            top: y - offset,
            strokeWidth: CIRCLE_THICKNESS,
            radius: CIRCLE_RADIUS,
            fill: TRANSPARENT_COLOR,
            stroke: CIRCLE_INACTIVE_COLOR
        });
        circle.hasBorders = circle.hasControls = false;
        circle.lockMovementX = true;
        circle.lockMovementY = true;
        circle.on({
            'selected': markSelectedCircle,
            'mousedown': moveSelectedCircle,
            'mouseup': save_state,
            'removed': save_state
        });
        canvas.add(circle);
        if(!force_route) {
            routes[active_route].push(circle);
            canvas.setActiveObject(circle);
            drawLines();
        } else {
            routes[force_route].push(circle);
        }
        return circle;
    }

    function moveSelectedCircle(e) {
        if(active_route == null) {
            this.lockMovementX = true;
            this.lockMovementY = true;
        }
    }
    function markSelectedCircle() {
        // console.log('markCircle()');
        if(active_route == null){
            alert("Välj en led först.");
            return;
        }
        unMarkCircle(selectedObject);
        if(typeof this.animate === "undefined"){return}
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
                // console.log("Marked circle already added to route");
                in_route = true;
            }
        });
        if(!in_route){
            // console.log("Adding marked route to active route!");
            routes[active_route].push(this);  //add to the active route.
            this.lockMovementX = false;
            this.lockMovementY = false;
            drawLines();
        }
        // console.log(routes);
    }

    function markActiveCircles() {
        // console.log('markActiveCircles()');
        $.each(routes, function (index, route) {
            $.each(route, function (index, circle) {
                circle.set('stroke', CIRCLE_INACTIVE_COLOR);
                circle.lockMovementX = true;
                circle.lockMovementY = true;
            });
        });
        $.each(routes[active_route], function (index, circle) {
            circle.set('stroke', CIRCLE_ACTIVE_COLOR);
            circle.lockMovementX = false;
            circle.lockMovementY = false;
        });
        canvas.renderAll();
    }

    function unMarkCircle(s) {
        // console.log('unMarkCircle()');
        if (s == null) {
            // console.log("- null");
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
        drawLines();
        // console.log("Activated route: " + route);
    }

    function drawLines(){

        function makeLine() {
            var line = new fabric.Line({
                fill: LINE_INACTIVE_COLOR,
                stroke: LINE_INACTIVE_COLOR,
                strokeWidth: LINE_THICKNESS,
                selectable: false
            });
            line.set('fill', LINE_INACTIVE_COLOR);
            line.set('stroke', LINE_INACTIVE_COLOR);
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

        // console.log("Draw lines!");
        $.each(routes, function (route_id, route) {


            if(!(route_id in lines)){
                lines[route_id] = [];
            }
            if(route.length <= 1) {
                return true;  //Breaks loop.
            }
            var line_num = lines[route_id].length;
            var route_num = routes[route_id].length;
            if(lines[route_id].length >= routes[route_id].length-1){
                //Delete has happened. Remove it all.
                $.each(lines[route_id], function (index, line) {
                    canvas.remove(line);
                });
                lines[route_id] = [];
            }

            for(var i = 1; i < (route.length); i++){
                var line = null;
                if(typeof lines[route_id][i-1] === 'undefined'){
                    line = makeLine();
                    setLineCoords(line, route[i-1], route[i]);
                    lines[route_id].push(line);
                    canvas.add(line);
                    line.sendToBack();
                    // console.log("Added line:");
                } else {
                    line = lines[route_id][i-1];
                    setLineCoords(line, route[i-1], route[i]);
                    if(route_id === active_route){
                        line.set('fill', LINE_ACTIVE_COLOR);
                        line.set('stroke', LINE_ACTIVE_COLOR);
                    } else {
                        line.set('fill', LINE_INACTIVE_COLOR);
                        line.set('stroke', LINE_INACTIVE_COLOR);
                    }
                }
            }
        });
        // console.log("RenderAll()");
        canvas.renderAll();
    }
    function save_state(){
        history.push(to_json());
        print(to_json());
        if (history.length > 50){
            history.reverse().pop();
            history.reverse();
        }
    }
    function undo_action(){
        if(history.length > 0){
            canvas.clear();
            for (var key in routes) {
                // skip loop if the property is from prototype
                if (!routes.hasOwnProperty(key)) continue;

                routes[key] = [];

            }
            var tmp = {};
            var json = JSON.parse(history.pop());
            $.each(json, function (route_id, route_data) {
                $.each(route_data, function (index, node) {
                    if(tmp.hasOwnProperty(node.left + "_" + node.top)){
                        routes[route_id].push(tmp[node.left + "_" + node.top]);
                    }
                    tmp[node.left + "_" + node.top] = addPoint(node.left, node.top, route_id);
                });
            });
            markActiveCircles();
            drawLines();
        }

    }
    function to_json(){
        var data = {};
        //Trouble to JSON-encode whole fabricjs object...
        $.each(routes, function (route_name, route_data) {
            if(route_data.length > 1){
                data[route_name] = [];
                $.each(route_data, function (index, circle) {
                    var tmp_obj = {
                        top: circle.top,
                        left: circle.left,
                        order: index
                    };
                    data[route_name].push(tmp_obj);
                });
            }
        });

        return JSON.stringify(data);

    }

    function save_data_cb(){
        var url = SAVE_ROUTE_NODE_URL + rockfaceimage_id + "/";
        var json_data = to_json();
        var success = function () {
            // console.log("Successfully saved data.");
        };
        $.ajax({
            type: "POST",
            url: url,
            contentType:'application/json',
            data: json_data,
            success: success,
            dataType: "json",
            async: true
        });
        // console.log("Saving data...");
    }

    function deleteNode(){
        if(selectedObject == null){return;}

        var to_delete = [];
        var new_arrays = {};

        //Search for references and filter away selected node.
        $.each(routes, function (route_id, route_array) {
            new_arrays[route_id] = $.grep(route_array, function (value) {
                return value !== selectedObject;
            });
        });
        //Replace old arrays.
        $.each(new_arrays, function (route_id, route_array) {
            routes[route_id] = route_array;
        });

        canvas.remove(selectedObject);
        selectedObject = null;  //Garbage collector remoces old circle?
        drawLines();

    }

    function init_csrf() {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = $.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }
    function init() {
        // console.log("Fabric loaded.");
        // console.log(rockface_id);
        init_csrf();
        get_data(rockface_id).done(function ( data ) {
            // console.log("Loaded rockface+image data.");
            // console.log(data);
            var old_nodes = data['old_nodes'];
            var w = data.image.image_width;
            var h = data.image.image_height;

            $.each(data.routes, function (index, route) {
                routes[route.id] = [];  //Make sure routes has an array for each route.
            });

            insert_dom_elements(w, h, data.routes, activate_route_cb, save_data_cb, undo_action);
            canvas = new fabric.Canvas("fabric_canvas");
            canvas.setBackgroundImage(data.image.image, canvas.renderAll.bind(canvas), {
                backgroundImageStretch: false
            });
            canvas.selection = false; //Disables box selection
            canvas.on({
                'mouse:down': onCanvasClick,
                'object:moving': drawLines
            });
            $('body').keyup(function (e) {
                if(e.keyCode === 46){  //46 = delete.
                    // console.log("delete node!");
                    deleteNode();
                }
            });
            //Add old nodes:
            function compare_nodes(a,b){
                if (a.order < b.order) {
                    return -1;
                } else if (a.order > b.order){
                    return 1;
                } else {
                    return 0;
                }

            }
            old_nodes.sort(compare_nodes);
            $.each(old_nodes, function (index, node) {
                var circle = addPoint(node.pos_x, node.pos_y, node.route_set[0]);
                if(node.route_set.length > 1) {
                    for (var i = 1; i < node.route_set.length; i++) {
                        var r_id = node.route_set[i];
                        routes[r_id].push(circle);
                    }
                }
            });
            drawLines();
            save_state();
        });
    }

//Start.
    rockface_id = $("div.field-rockface_key").children("div").children("p").text();
    rockfaceimage_id = $("div.field-id").children("div").children("p").text();
    if(rockface_id && rockfaceimage_id){
        $.getScript('https://cdnjs.cloudflare.com/ajax/libs/fabric.js/1.6.2/fabric.min.js', init);
    } else {
        // console.log("No id found.");
    }
});


