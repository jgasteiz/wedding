(function () {
    'use_strict';

    $('.html-field').each(function () {
        var index = $(this).data('index'),
            editor = ace.edit('html-' + index),
            textarea = $(this).find('textarea'),
            $iframe = $('#html-preview-' + index);

        editor.setTheme("ace/theme/monokai");
        editor.getSession().setMode("ace/mode/html");
        editor.getSession().setValue(textarea.val());
        editor.getSession().on('change', function(){
            var html = editor.getSession().getValue();
            textarea.val(html);
            $iframe.contents().find("body").html(html);
        });

        $iframe.contents().find("body").html(textarea.val());
    });
})();
