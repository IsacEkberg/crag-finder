/**
 * Created by jonathan on 2016-04-14.
 */

$ = django.jQuery;

$('document').ready(function(){
    $('#image-group').append('<div class="submit-row" style="margin-top: 30px"><p style="float: left;">Du måste trycka på "Spara och fortsätt redigera" om du laddat upp en bild i steget ovan för att kunna välja den till lederna.</p><input type="submit" value="Spara och fortsätt redigera" name="_continue"></div>');
});
