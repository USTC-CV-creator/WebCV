// post json and read returned json
jQuery.api_post = function ( url, data, success, fail ) {
    'use strict';
    var ajax_opt = {
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify( data ),
        contentType: 'application/json',
        success: function ( data, status ) {
            if ( $.isFunction( success ) ) {
                success( data, status );
            }
        },
        error: function () {
            if ( $.isFunction( fail ) ) {
                fail();
            }
        }
    };
    $.ajax( url, ajax_opt );
};
