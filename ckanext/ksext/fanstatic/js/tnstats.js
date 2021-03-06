var config = { };

$(document).ready(function (){
    config = getConfig($('#hidConfig').val());

    $('.module-narrow li.nav-item').removeClass('active').filter(function (i,d){ 
        return i===config.menuIndex;
    }).addClass('active');

    mainColumnMerge();

    $(config.selectId).change(orgChanged);
    $('#btnDownload').click(function (){
        if(!$(config.selectId).val())
            window.open(config.windowOpenUrl);
        else window.open(config.windowOpenUrl + $(config.selectId).val());
    });
});

function getConfig(val){
    if(val === 'org'){
        return {
            menuIndex: 0,
            selectId:'#selOrg',
            title: 'org_name',
            dataUrl: '/tnstats/orgApi?id=',
            windowOpenUrl :'/tnstats/orgCsv?id='
        }
    }else if(val === 'group'){
        return {
            menuIndex: 1,
            selectId:'#selGroup',
            title: 'group_name',
            dataUrl: '/tnstats/groupApi?id=',
            windowOpenUrl :'/tnstats/groupCsv?id='
        }
    }else{
        return {
            menuIndex: 4,
            selectId:'#selDataset',
            title: 'dataset_name',
            dataUrl: '/tnstats/datasetApi',
            windowOpenUrl :'/tnstats/datasetCsv'
        }
    }
}

function orgChanged(evt){
    var url = config.dataUrl + evt.target.value;
        $.post(url, function (res){
            console.log(res);
            RemoveTr();
            var tb = $("#dtStat");
            $(res).each(function (i, d){
                var aps = '<tr>';
                aps += '<td class="metric">' + d[config.title] + '</td>';
                aps += '<td><a href="/dataset/' + d.name + '">'+ d.title + '</a></td>';
                aps += '<td class="metric">' + d.dataset_views + '</td>';
                aps += '<td class="metric">' + d.resource_views + '</td>';
                aps += '<td class="metric">' + d.resource_downloads + '</td>';
                aps += '</tr>';
                tb.append(aps);
            });
            mainColumnMerge();
        });
}

function RemoveTr(){
    $("#dtStat tr").each(function (i, d) {
        if(i==0) return;
        $(d).remove();
    });
}

function mainColumnMerge(){

    var checkName = '',
        rowCount = 1,
        checkTd = null;

    $('#dtStat tr').each(function(i, d) {
        if (i == 0) return;
        var td = $(d).children().first();
        if (td.html() != checkName) {
            checkName = td.html();
            if (checkTd) {
                checkTd.attr("rowspan", rowCount);
            }
            rowCount = 1;
            checkTd = td;
        } else {
            td.remove();
            rowCount++;
        }
    });
    if(checkTd){
        checkTd.attr("rowspan", rowCount);
    }
}