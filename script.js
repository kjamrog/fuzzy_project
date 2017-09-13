
$(document).ready(function(){
    $('.parametersInput').submit(function(event){
        event.preventDefault();
        console.log('hello');
        console.log($('.parametersInput').serialize());
        $.ajax({
            type: 'POST',
            url: '/cgi-bin/fuzzy_project/cgi_script.py',
            data: $('.parametersInput').serialize(),
            success: function(data){
                $('#response').html(data);
            },
            error: function(jqXHR, textStatus, err){
                console.log('jqXHR:', jqXHR);
                console.log('textStatus:', textStatus);
                console.log('err:', err);
            }
        });
    });
});
