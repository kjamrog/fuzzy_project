
$(document).ready(function(){
    $('.priceInput').submit(function(event){
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: './main.py',
            data: $('.priceInput').serialize(),
            success: function(data){
                console.log(data)
            },
            error: function(jqXHR, textStatus, err){
                console.log(err);
            }
        });
    });
});
