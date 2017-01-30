(function ($) {
    $(document).ready(function ($) {
        var i = 0;
        $('table tr').each(function () {
            if (i == 0) {
                var trHtml = "<th>状态</th>";
                $(this).append(trHtml);
            }
            if (i != 0 && this.children.length > 2) {
                var trHtml = "<td><div id='jqmeter-container'></div></td>";
                $(this).append(trHtml);

            }
            i++;
        });

    });

    $(document).ready(function () {
        $('#jqmeter-container').jQMeter();
    });
})(django.jQuery);