(function ($) {
    $(document).ready(function ($) {
        addCol()
    });

    function addCol() {
        var colCount = 0;
        $("#result_list tr").each(function () {
            var trHtml = $(this).html();
            if (colCount == 0) {
                trHtml += '<th>操作</th>';
            } else {
                var id = $(trHtml)[0].children[0].value;
                trHtml += '<td><button onclick="runScript(' + id + ')"  class="button" type="button">执行</button></td>';
            }

            $(this).html(trHtml);
            colCount++;
        });
    }

})(django.jQuery);


function runScript(id) {
    alert(id)
}
