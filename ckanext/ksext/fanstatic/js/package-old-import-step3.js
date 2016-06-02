$(function (){
    
    var url = '/api/3/action/package_show?id=' + $('#field-extras-9-value').val();
    $.post(url, function (res){
        if(!res || !res.success){
            return;
        }

        var extras = res.result.extras;
        var keys = ['更新頻率', '收錄期間（起）', '收錄期間（迄）', '提供機關聯絡人電話', '提供機關地址'];
        var ids = ['#field-extras-4-value', '#field-extras-5-value', '#field-extras-6-value', '#field-extras-7-value', '#field-extras-8-value'];
        
        for (var i=0; i<keys.length;i++){
            setExtra(extras, keys[i], ids[i]);
        }

        $('#field-url').val(res.result.url);
        $('#field-maintainer').val(res.result.maintainer);
        $('#field-maintainer-email').val(res.result.maintainer_email);
    });

    function setExtra(list, key, id){
        var extra = findProp(list, 'key', key);
        $(id).val(
            extra && extra.length>0 
            ? extra[0].value
            : ''
        );
    }
    function findProp(list, key, propName){
        return $.grep(list, function(item){
            return item[key] === propName;
        });
    };
});
