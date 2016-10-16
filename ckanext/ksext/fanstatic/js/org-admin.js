$(function (){
    //alert('ready');
    var org_id = hidOrgId.value;
    console.log(org_id);

    $('.org-admin').click(function (evt){
        var target = $(evt.target);
        var package_id = target.data("package_id");
        console.log(package_id);
    });
});
