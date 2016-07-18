// select text on an elem
// http://stackoverflow.com/a/2838358
jQuery.fn.selectText = function () {
    'use strict';
    var el = this[ 0 ];
    var doc = window.document;
    var range;
    if ( window.getSelection && doc.createRange ) {
        var sel = window.getSelection();
        range = doc.createRange();
        range.selectNodeContents( el );
        sel.removeAllRanges();
        sel.addRange( range );
    } else if ( doc.body.createTextRange ) {
        range = doc.body.createTextRange();
        range.moveToElementText( el );
        range.select();
    }
    return this;
};
