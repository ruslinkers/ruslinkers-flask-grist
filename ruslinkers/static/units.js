$(document).ready(function () {
    var $container = $('#sidebar'),
        $scrollTo = $('a.active');
    $container.scrollTop(
        $scrollTo.offset().top - $container.offset().top + $container.scrollTop()
    );

    $('#filter-linkers').on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#sidebar a").filter(function () {
            $(this).toggle($(this).children('div.linker-name').text().toLowerCase().indexOf(value) > -1)
        });
    });

    $('#exampleTable').DataTable();

    // Event handlers for setting attributes of objects
    $("input.setattr").on("input", function () {
        let target_id = $(this).attr("data-target_id");
        let target_type = $(this).attr("data-target_type");
        let attr = $(this).attr("data-attr");
        let btn = $(`button.setattr[data-target_id='${target_id}'][data-target_type='${target_type}'][data-attr='${attr}']`);
        btn.removeClass("d-none");
    });
    $("button.setattr").on("click", function () {
        $(this).addClass("d-none");
        let target_id = $(this).attr("data-target_id");
        let target_type = $(this).attr("data-target_type");
        let attr = $(this).attr("data-attr");
        let input = $(`input.setattr[data-target_id='${target_id}'][data-target_type='${target_type}'][data-attr='${attr}']`)
        $.post("units.html", { action: 'setattr', target_id: target_id, target_type: target_type, attr: attr, newvalue: input.val() });
        const toast = bootstrap.Toast.getOrCreateInstance($("div#updateToast"));
        toast.show();
    })
    // Event handlers for adding objects
    $("button.addform").on("click", function () {
        let unit_id = $(this).attr("data-unit_id");
        let formtype = $(this).attr("data-formtype");
        let input = $(`input.addform[data-unit_id='${unit_id}'][data-formtype='${formtype}']`);
        $.post("units.html", { action: "addform", unit_id: unit_id, formtype: formtype, text: input.val() })
    });
    // Delete object
    $("button.delobject").on("click", function () {
        let target_id = $(this).attr("data-target_id");
        let target_type = $(this).attr("data-target_type");
        $.post("units.html", { action: "delobject", target_id: target_id, target_type: target_type })
    });

    // Search stuff
    $(".toggleSearch").on("change", function () {
        target = $('#' + $(this).attr('data-toggle'));
        console.log(target);
        if(this.checked) {
            target.removeAttr('disabled');
        }
        else {
            target.attr('disabled','true');
        }
    });

    $("#searchButton").on("click", function() {
        let params="";
        $(".searchData").each(function(i, obj) {
            if(!obj.hasAttribute('disabled')) {
                params += '?' + obj.id + '=' + $(this).val();
            }
        })
        window.location.href = window.location.href.split(/[?#]/)[0] + params;
    })
});