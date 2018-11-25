
/*$(function()
{
    function after_form_submitted(data) 
    {
        if(data.result == 'success'){
            $('form#reused_form').hide();
            $('#success_message').hide();
            $('#error_message').hide();
            $('*').css('background', 'transparent');
            $('#mainbody').html(data.htmlcontent);
        }
        else if(data.result == 'pending'){
            alert("aaaa");
        }
        
        else{
            $('#error_message').append('<ul></ul>');
            jQuery.each(data.errors,function(key,val)
            {
                $('#error_message ul').append('<li>'+key+':'+val+'</li>');
            });
            $('#success_message').hide();
            $('#error_message').show();

            //reverse the response on the button
            $('button[type="button"]', $form).each(function()
            {
                $btn = $(this);
                label = $btn.prop('orig_label');
                if(label)
                {
                    $btn.prop('type','submit' ); 
                    $btn.text(label);
                    $btn.prop('orig_label','');
                }
            });
        }
    }

    $('#reused_form').submit(function(e)
    {
        e.preventDefault();

        $form = $(this);

        //show some response on the button
        $('button[type="submit"]', $form).each(function()
        {
            $btn = $(this);
            $btn.prop('type','button' ); 
            $btn.prop('orig_label',$btn.text());
            $btn.text('Sending ...');
        });
        
        $.ajax({
                type: "POST",
                url: 'polls/crawl',
                data: $form.serialize(),
                success: after_form_submitted,
                dataType: 'json' 
        });       
    });
});
*/

$(document).ready(function(){
    function after_form_submitted(data) 
    {
        alert('aaa');
        setTimeout(function(){autoCall();}, 5000);
    }

    $('#reused_form').submit(function autoCall(e)
    {
        e.preventDefault();

        $form = $(this);

        //show some response on the button
        $('button[type="submit"]', $form).each(function()
        {
            $btn = $(this);
            $btn.prop('type','button' ); 
            $btn.prop('orig_label',$btn.text());
            $btn.text('Sending ...');
        });
        
        $.ajax({
                type: "POST",
                url: 'polls/crawl',
                data: $form.serialize(),
                success: after_form_submitted,
                dataType: 'json',
                async: false
        });       
    });
    //$('div').html(feedback);
});