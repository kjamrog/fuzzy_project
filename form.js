
$(document).ready(function(){
    $('.priceInput').submit(function(event){
        event.preventDefault();
        console.log('fdsafdasfdsfsdaf');
        console.log($('.priceInput').serialize());
        $.ajax({
            type: 'POST',
            url: '/cgi-bin/fuzzy_project/cgi_script.py',
            data: $('.priceInput').serialize(),
            success: function(data){
                console.log('****', data);
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
