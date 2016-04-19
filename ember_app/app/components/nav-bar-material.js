import Ember from 'ember';
var $ = Ember.$;


export default Ember.Component.extend({
  transparent: true,
  didRender() {
    this._super(...arguments);




  },

  materialKit(debounce, transparent, big_image) {
    return {
      misc: {
        navbar_menu_visible: 0
      },

      checkScrollForTransparentNavbar: debounce(function () {
        if ($(document).scrollTop() > 260) {
          if (transparent) {
            transparent = false;
            $('.navbar-color-on-scroll').removeClass('navbar-transparent');
          }
        } else {
          if (!transparent) {
            transparent = true;
            $('.navbar-color-on-scroll').addClass('navbar-transparent');
          }
        }
      }, 17),

      initSliders: function () {
        // Sliders for demo purpose
        $('#sliderRegular').noUiSlider({
          start: 40,
          connect: "lower",
          range: {
            min: 0,
            max: 100
          }
        });

        $('#sliderDouble').noUiSlider({
          start: [20, 60],
          connect: true,
          range: {
            min: 0,
            max: 100
          }
        });
      },
      checkScrollForParallax: debounce(function(){
        console.log("Checking scroll.");
        //var current_scroll = $(this).scrollTop();

        var oVal = ($(window).scrollTop() / 3);

        big_image[0].css({
            'transform':'translate3d(0,' + oVal +'px,0)',
            '-webkit-transform':'translate3d(0,' + oVal +'px,0)',
            '-ms-transform':'translate3d(0,' + oVal +'px,0)',
            '-o-transform':'translate3d(0,' + oVal +'px,0)'
        });

        }, 6)
    };
  },

  debounce(func, wait, immediate) {
      var timeout;
      return function () {
        var context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function () {
          timeout = null;
          if (!immediate) { func.apply(context, args); }
        }, wait);
        if (immediate && !timeout) { func.apply(context, args); }
      };
    }
});
