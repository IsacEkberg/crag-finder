/**
 * Created by isac on 2016-03-30.
 */


if(!$){
    $ = django.jQuery;
    $('document').ready(function(){

        function init(){
            prevoiusValues = getPreviousInput();
            s = $input.val();
            var center_coord;
            var zoon_level;
            if(!s){
                zoon_level = 6;
                center_coord = {lat: 60.662, lng: 15.681};
            } else {
                var point = s.split(";")[0];
                var lat_lng = point.substring(1, point.length-1).split(", ");
                zoon_level = 14;
                center_coord = {lat: Number(lat_lng[0]), lng: Number(lat_lng[1])};
            }
            map = new google.maps.Map(document.getElementById('map'), {
               zoom: zoon_level,
               center: center_coord
            });

            poly = new google.maps.Polyline({
                path: prevoiusValues,
                strokeColor: '#000000',
                strokeOpacity: 1.0,
                strokeWeight: 3,
                editable: true
            });
            /*
            if (prevoiusValues){
                console.log("Previous values!");
                poly.setPath(prevoiusValues);
            }
            */
            poly.setMap(map);

            google.maps.event.addListener(poly, 'rightclick', removeVertex);
            //Mouseup is not perfect...
            google.maps.event.addListener(poly, 'mouseup', updateInput);
            google.maps.event.addListener(poly, 'drag', updateInput);
            // Add a listener for the click event
            map.addListener('click', addLatLng);
            setInterval(updateInput, 5000)
        }
        function removeVertex(e) {
            if (e.vertex == undefined) {
                return;
            }
            var path = poly.getPath();
            path.removeAt(e.vertex);
            updateInput();

        }

        function addLatLng(event) {
            var path = poly.getPath();

            // Because path is an MVCArray, we can simply append a new coordinate
            // and it will automatically appear.
            path.push(event.latLng);
            updateInput();
        }

        function updateInput() {
            var path = poly.getPath();
            var s = "";
            path.forEach(function(ele, index){
               s = s + ele + ";";
            });
            $input.val(s);
        }

        function getPreviousInput(){
            s = $input.val();
            if(!s){
                return
            }
            arr = s.split(";");
            arr2 = [];
            $.each(arr,function( index, value2 ) {
                if(value == "") {return;}
                var value = value2.substring(1, value2.length-1);
                vals2 = value.split(", ");
                if(vals2 == "") {return;}
                arr2.push({lat:parseFloat(vals2[0]), lng:parseFloat(vals2[1])})
            });
            return arr2;
        }


        $input = $("#id_geo_data");
        $input.parent().append("<div id='map'></div>");

        $.getScript("https://maps.googleapis.com/maps/api/js?key=AIzaSyD3sdImCNCvjYXzqlePVqJ8u08alKCVKs0", init);

        })
}
