/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function ( config ) {

    // prevent ckeditor from adding <p>
    config.enterMode = CKEDITOR.ENTER_BR;
    // prevent ckeditor from removing elements.
    config.allowedContent = true;
    // disable table borders
    config.startupShowBorders = false;
    config.resize_enabled = true;

    // below is auto generated using samples/toolbarconfigurator/index.html
    config.toolbarGroups = [
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
        { name: 'links', groups: [ 'links' ] },
        { name: 'insert', groups: [ 'insert' ] },
        { name: 'forms', groups: [ 'forms' ] },
        { name: 'tools', groups: [ 'tools' ] },
        { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
        { name: 'others', groups: [ 'others' ] },
        { name: 'about', groups: [ 'about' ] },
        '/',
        { name: 'styles', groups: [ 'styles' ] },
        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
        { name: 'colors', groups: [ 'colors' ] }
    ];

    config.removeButtons = 'Underline,SpecialChar,Maximize,Source,Scayt,Cut,Copy,Anchor,Strike,Blockquote,Image';
};
