$(function (){
    //alert('ready');
    var org_id = hidOrgId.value;
    console.log(org_id);

    $('.org-admin').click(function (evt){
        var target = $(evt.target);
        var package_id = target.data("package_id");
        hidCurrentPackage.value=package_id;
        console.log(package_id);
        $.ajax({
            url: "/orgadmin",
            type: "get",
            dataType: "json",
            data: {
                org: org_id,
                ds: package_id
            },
            success: getOrgAdminResponse,
            error: function(xhr) {
            //Do Something to handle error
            }
        });
    });

    $('#btnModalUpdate').click(function (){
        var p = {
           user: selOrgUsers.value,
           ds: hidCurrentPackage.value
        };
        console.log(p);
        $.ajax({
            url: "/orgadmin/update",
            type: "post",
            dataType: "json",
            data: p,
            success: function (response){
                //console.log(response);
                if(response.success){
                    alert('修改完成！')
                    location.reload();
                } else{
                    alert('更新失敗！')
                }
            },
            error: function(xhr) {
            //Do Something to handle error
            }
        });
    });

    function getOrgAdminResponse(response){
        console.log(response);
        $('#lblAdminUser').html(response.manager[0].name);
//<option value="4f3804fe-9bc3-45f5-8f33-ee6294d46d9c">geo-org</option>
        var opt = response.org_users.map(function (d){
            return '<option value="' + d.id + '" >' + d.name + '</option>';
        });
//console.log(opt);
        $('#selOrgUsers').empty().append(opt.join(''));
        $('#adminModal').modal('show');
    }
});
