(function () {
    'use_strict';

    var editor = ace.edit("html");
    var textarea = $('textarea[name="html"]');
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/html");
    editor.getSession().setValue(textarea.val());
    editor.getSession().on('change', function(){
      textarea.val(editor.getSession().getValue());
    });
})();
