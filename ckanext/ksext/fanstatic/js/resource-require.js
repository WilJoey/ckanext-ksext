    var checkAddId = ['field-name','field-description','field-format'];
    var checkAddMsg = ['資料名稱','主要欄位說明','檔案格式'];

    $(document).ready(function (){
      $('.btn-require').click(function(){
        for(var i in checkAddId){
          var item=$("#"+checkAddId[i]);
          if(item.val().trim()==''){
            item.focus();
            alert("欄位 [" + checkAddMsg[i] + "] 必填!");
            return false;
          }
        }
        return true;
      });
    });