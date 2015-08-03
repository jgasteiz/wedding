(function () {
    'use_strict';

    var editor = ace.edit('html'),
        textarea = $('textarea[name="html"]'),
        $iframe = $('#html-preview');

    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/html");
    editor.getSession().setValue(textarea.val());
    editor.getSession().on('change', function(){
        var html = editor.getSession().getValue();
        textarea.val(html);
        $iframe.contents().find("body").html(html);
    });

    $iframe.contents().find("body").html(textarea.val());
})();
