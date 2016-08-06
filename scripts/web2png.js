"use strict";
var page = require( 'webpage' ).create(),
    system = require( 'system' ),
    address, output, width;

if ( system.args.length != 4 ) {
    console.log( 'Usage: gen_thumbnail.js URL filename pixel_width' );
    phantom.exit( 1 );
} else {
    address = system.args[ 1 ];
    output = system.args[ 2 ];
    width = parseInt( system.args[ 3 ] );

    try {
        page.open( address, function ( status ) {
            if ( status !== 'success' ) {
                console.log( 'Unable to load the address!' );
                phantom.exit( 2 );
            } else {
                window.setTimeout( function () {
                    var page_size = page.evaluate( function () {
                        var $html = $( 'html' );
                        return [ $html.width(), $html.height() ];
                    } );
                    var factor = width / page_size[ 0 ];
                    page.viewportSize = {
                        width: page_size[ 0 ] * factor,
                        height: page_size[ 1 ] * factor
                    };
                    page.zoomFactor = factor;
                    page.render( output );
                    phantom.exit();
                }, 200 );
            }
        } );
    } catch ( e ) {
        phantom.exit( 3 );
    }
}
