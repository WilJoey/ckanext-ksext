$(function(){

    $('#field-organizations').change(function (){
    
        var url = '/api/3/action/organization_show?id=' + $('#field-organizations').val();
        $.post(url, function (res){
            var ds = $('#selDatasets');
            ds.empty();
            if(!res.success){
                //alert('請先選擇組織機關');
                return;
            }
            
            __importDataSets = res.result.packages;
            
            $.each(__importDataSets,function (i, d){
                ds.append(new Option(d.title, d.id));
            });
        });
    }).change();
});
var __importDataSets;
function _dsImport(){
    var ps = findProp(__importDataSets, 'id', $('#selDatasets').val());
    if(!ps){
        return;
    }
    var ds = ps[0];
    // delete ds.organization;
    // delete ds.resources;
    // delete ds.tags;
    // delete ds.tracking_summary;
    // delete ds.relationships_as_object;
    // delete ds.relationships_as_subject;
    $('#field-extras-9-value').val(ds.id);
    var exs = ds.extras ;
    var keys = ['資料集類型', '授權說明網址', '計費方式'];
    var ids = ['#field-extras-0-value', '#field-extras-2-value', '#field-extras-3-value'];
    
    for (var i=0; i<keys.length;i++){
        setExtra(exs, keys[i], ids[i]);
    }
    // var extras0 = findProp(exs, 'key', '資料集類型');
    // $('#field-extras-0-value').val(
    //     extras0 && extras0.length>0 
    //     ? extras0[0].value
    //     : ''
    // );
    
    // var extras2 = findProp(exs, 'key', '授權說明網址');
    // $('#field-extras-2-value').val(
    //     (extras2 && extras2.length > 0)
    //     ? extras2[0].value
    //     : ''
    // );

    // var extras3 = findProp(exs, 'key', '計費方式');
    // $('#field-extras-3-value').val(
    //     (extras3 && extras3.length > 0)
    //     ? extras3[0].value
    //     : ''
    // );
    
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
}



