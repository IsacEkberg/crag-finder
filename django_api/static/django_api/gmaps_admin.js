/**
 * Created by isac on 2016-03-30.
 */


if(!$){
    $ = django.jQuery;
    $('document').ready(function(){
        console.log("Haj!");

        function init(){
            console.log("Haj2!");
            prevoiusValues = getPreviousInput();
            map = new google.maps.Map(document.getElementById('map'), {
               zoom: 6,
               center: {lat: 60.662, lng: 15.681}  // Center the map on Chicago, USA.
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
            console.log("Haj2.5");
            if (e.vertex == undefined) {
                return;
            }
            console.log("Haj3");
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
            console.log("Update!");
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
                console.log("No previous data");
                return
            }
            arr = s.split(";");
            console.log(arr);
            arr2 = [];
            $.each(arr,function( index, value2 ) {
                if(value == "") {return;}
                var value = value2.substring(1, value2.length-1);
                vals2 = value.split(", ");
                if(vals2 == "") {return;}
                arr2.push({lat:parseInt(vals2[0]), lng:parseInt(vals2[1])})
            });
            console.log(arr2);
            return arr2;
        }


        $input = $("#id_geo_data");
        $input.parent().append("<div id='map'></div>");

        $.getScript("https://maps.googleapis.com/maps/api/js?key=AIzaSyD3sdImCNCvjYXzqlePVqJ8u08alKCVKs0", init);

        })
}
