(function ($) {
    $(document).ready(function ($) {
        var i = 0;
        $('table tr').each(function () {
            if (i != 0 && this.children.length > 2) {
                $(this.children[2].children[0]).on('click', function () {
                    var j = 0;
                    var _this = this;
                    $('table tr').each(function () {
                        if (j != 0 && this.children.length > 2) {
                            debugger;
                            if ($(this.children[2].children[0])[0] != _this) {
                                $(this.children[2].children[0]).removeAttr("checked")
                            }
                        }
                        j++
                    });
                });
            }
            i++;
        });

        // var addNewBtn = $(".add-row")[0].children[0].children[0]
        // $(addNewBtn).on('click', function () {
        //     $("input[type='checkbox']").removeAttr("checked");
        // });

    });
})(django.jQuery);