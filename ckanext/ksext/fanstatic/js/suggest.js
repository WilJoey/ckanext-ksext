$(document).ready(function (){
    $('.domail').click(function (evt){
        var target = $(evt.target);
        target.prop('disabled', true);
        var id = target.data('suggest_id');

        $.post('/suggest/domail/'+id, function(data){
            if(!data.Success){
                alert('信件寄送失敗！')
            } else{
                alert('信件已寄送！')
                location.reload();
            }
        });
    });
});

function views_plus(id){
    $.post('/suggest/view/'+id, function(data){});
    return true;
}
