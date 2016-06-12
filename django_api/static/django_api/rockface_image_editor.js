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
    var canvas = null;
    
    function init() {
        console.log("Fabric loaded.");
        var object_id = $("div.field-rockface_key").children("div").children("p").text();
        console.log(object_id);
        
        get_data(object_id).done(function ( data ) {
            console.log("Loaded rockface+image data.");
            console.log(data);
            var w = data.image.image_width;
            var h = data.image.image_height;
            function test_cb(text){
                console.log(text);
            }
            insert_dom_elements(w, h, data.routes, test_cb);
            canvas = new fabric.Canvas("fabric_canvas");
            canvas.setBackgroundImage(data.image.image, canvas.renderAll.bind(canvas), {
                backgroundImageStretch: false
            });
        });
    }

    //TODO: Get: image-url, image-size, rockface-routes, route-nodes.
    console.log("Hello, world.");
    $.getScript('https://cdnjs.cloudflare.com/ajax/libs/fabric.js/1.6.2/fabric.min.js', init);
});


