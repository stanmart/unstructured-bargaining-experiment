$('input').bind('keypress', function(e) {
    if(e.keyCode === 13 || e.key == 'Enter') {
       return false;
    }
});
