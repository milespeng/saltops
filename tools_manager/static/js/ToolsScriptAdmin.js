(function ($) {
    $(document).ready(function ($) {
        $('.inline_label').remove()
        $('#toolsscript_form').append("<input type='text' style='display: none' id='action' name='action' value='0'></input>")
        $('.submit-row').before("<button onclick='setValue()' type='button'  class='btn btn-high'>执行工具</button>")
        sls_host = $('.field-hosts')[0].children[0].children[1].children[0].children[0]
        for (var i = 0; i < $(sls_host)[0].options.length; i++) {
            $(sls_host)[0].options[i].selected = false
        }

        $('#id_toolsexecjob_set-0-param').val("")
    });

// function addCol() {
//     var colCount = 0;
//     $("#result_list tr").each(function () {
//         var trHtml = $(this).html();
//         if (colCount == 0) {
//             trHtml += '<th>操作</th>';
//         } else {
//             var id = $(trHtml)[0].children[0].value;
//             trHtml += '<td><button onclick="runScript(' + id + ')"  class="button" type="button">执行</button></td>';
//         }
//
//         $(this).html(trHtml);
//         colCount++;
//     });
// }

})
(django.jQuery);


function setValue() {
    document.getElementById("action").value = 1;
    document.getElementById("toolsscript_form").submit();
}
