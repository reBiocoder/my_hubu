$(function () {
    var allBrash = ['js', 'xml', 'java', 'c', 'ruby', 'csharp', 'css', 'delphi', 'erlang', 'groovy', 'javafx', 'perl', 'php', 'powershell', 'python', 'scala', 'sql', 'vb', 'as3', 'bash', 'coldfusion', 'diff', 'plain', 'sass'];
    var laguage=$("pre code").attr('class');
    if (laguage==undefined)
    {
        $('pre').attr('class', 'brush:python;');
                var htmlCode = $('code').html();
                $('code').remove();
                $('pre').html(htmlCode);
                SyntaxHighlighter.config.strings = {help: '?',};
                SyntaxHighlighter.all();
    }
    else {
        var result = laguage.split('-');
        var code = result[1];
        for (var i = 0; i < allBrash.length; i++) {
            if (code == allBrash[i]) {
                $('pre').attr('class', 'brush:' + code + ';');
                var htmlCode = $('code').html();
                $('code').remove();
                $('pre').html(htmlCode);
                SyntaxHighlighter.config.strings = {help: '?',};
                SyntaxHighlighter.all();
                break;
            } else {
                $('pre').attr('class', 'brush:python;');
                var htmlCode = $('code').html();
                $('code').remove();
                $('pre').html(htmlCode);
                SyntaxHighlighter.config.strings = {help: '?',};
                SyntaxHighlighter.all();
            }

        }
    }
});
