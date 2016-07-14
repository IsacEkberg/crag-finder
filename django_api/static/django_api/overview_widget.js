/**
 * Created by isac on 2016-07-13.
 */

/* globals $: true */
/* globals django: false */
/* globals fabric: false */

if(!$) {
    $ = django.jQuery;
}

$('document').ready(function(){
    var nrFaces = $('fieldset.module.aligned.hidden')
        .children("div.form-row.field-faces")
        .children("div")
        .children("p")
        .text();
    var $p_sector = $("<p>");
    var $new_UI_element = $("<div>");
    $new_UI_element.attr('class', 'description');
    var $target_parent = $("div#content");

    if(nrFaces === "0"){
        $p_sector.text("Inga sektorer är tillagda. Skapa en ny längst ned på denna sida.");
        $p_sector.attr('class', 'warning');
    } else {
        var s = "Det finns ";
        s += nrFaces;
        s += " sektorer inlagda. Du hittar dessa i menyn 'områdesöversikt' ovan.";
        $p_sector.text(s);
    }

    $new_UI_element.append($p_sector);
    $target_parent.children("h1").first().after($new_UI_element);
});