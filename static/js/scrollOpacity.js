$(window).scroll(function() {
    var scrollTop = $(this).scrollTop();
  
    $('#searchBar').css({
      opacity: function() {
        var elementHeight = $(this).height();
        return 0 + (elementHeight - scrollTop) / elementHeight;
      }
    });
  });