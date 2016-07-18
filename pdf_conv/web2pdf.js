"use strict";
var page = require( 'webpage' ).create(),
    system = require( 'system' ),
    address, output;

if ( system.args.length !== 3 ) {
    console.log( 'Usage: phantomjs --disk-cache=yes web2pdf.js URL filename' );
    phantom.exit( 1 );
} else {
    address = system.args[ 1 ];
    output = system.args[ 2 ];
    page.viewportSize = { width: 600, height: 600 };
    page.paperSize = { format: 'A4', orientation: 'portrait', margin: 0 };
    page.open( address, function ( status ) {
        if ( status !== 'success' ) {
            console.log( 'Unable to load the address!' );
            phantom.exit( 2 );
        } else {
            // adjust timeout here
            window.setTimeout( function () {
                page.render( output );
                phantom.exit();
            }, 500 );
        }
    } );
}
