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
    $.getJSON('/api/v1/rockfaces/' + id)
        .done(function ( data ) {
            var rockface_data = data;
            return $.getJSON('http://127.0.0.1:1337/api/v1/rockfaceimages/?rockface=' + id)
            .done(function (rockfaceimage_data) {
                data_promise.resolve({
                    rockface: rockface_data,
                    image: rockfaceimage_data[0]  //Is it always only one rockface image? (REST API returns a list)
                });
            });
        });
    return data_promise;
    }

function insert_canvas(w, h) {
    var el = "<canvas id=\"fabric_canvas\" width=\"" + w + "\" height=\"" + h + "\"></canvas>";
    $("div#content-main").prepend(el);
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
            insert_canvas(w, h);
            canvas = new fabric.Canvas("fabric_canvas");
            canvas.setBackgroundImage(data.image.image, canvas.renderAll.bind(canvas), {
                backgroundImageStretch: false
            });
            //fabric.Image.fromURL(data.image.image, function(img) {
            //    canvas.setBackgroundImage = img;
                //canvas.backgroundImage.width = w;
                //canvas.backgroundImage.height = h;

                //canvas.add(img);
            //});

        });
    }

    //TODO: Get: image-url, image-size, rockface-routes, route-nodes.
    console.log("Hello, world.");
    $.getScript('https://cdnjs.cloudflare.com/ajax/libs/fabric.js/1.6.2/fabric.min.js', init);
});


