$(document).ready(function () {
    // Add scrollspy
    const scrollSpy = new bootstrap.ScrollSpy("#text-moreDB", {
        target: '#navbar-moreDB'
    });

    $('#moreDB').on("shown.bs.modal", function () {
        scrollSpy.refresh();
    });
    $('#semfield-list').on("shown.bs.collapse", function () {
        scrollSpy.refresh();
    })

    var $container = $('#sideView'),
        $scrollTo = $('a.lnkr.active');
    // $container.scrollTop($scrollTo.position().top + $container.scrollTop());
    if($scrollTo.length > 0) {
    $container.scrollTop(
        $scrollTo.offset().top - $container.offset().top + $container.scrollTop()
    );}

    $('#filter-linkers').on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#sidebar a").filter(function () {
            $(this).toggle($(this).children('div.linker-name').text().toLowerCase().indexOf(value) > -1)
        });
    });

    // Search stuff

    // Toggle enabled/disabled for search fields
    $(".toggleSearch").on("change", function () {
        target = $('#' + $(this).attr('data-toggle'));
        if (this.checked) {
            target.removeAttr('disabled');
            if (target.is(".btn-check[id^='search-']")) {
                target.trigger('change');
            }
        }
        else {
            target.attr('disabled', 'true');
            if (target.is(".btn-check[id^='search-']")) {
                $(`#${target.attr('id')}-un`).prop('disabled',true);
            }
        }
    });

    // When toggles are pressed
    $(".toggleSearch-select").on("change", function () {
        // target = $(`button[data-id="${$(this).attr('data-toggle')}"]`);
        target = $('#' + $(this).attr('data-toggle'));
        if (this.checked) {
            target.prop('disabled', false);
            target.selectpicker('setStyle','btn-outline-primary');
            target.selectpicker('refresh');
            // target.trigger('change');
        }
        else {
            target.prop('disabled', true);
            target.selectpicker('setStyle','btn-outline-primary','remove');
            target.selectpicker('refresh');
            // target.trigger('change');
        }
    });

    // Button toggles with custom changing text. Note the use of invisible fields, otherwise toggles don't send info when unchecked
    $(".btn-check[id^='search-']").on("change", function () {
        if (this.checked) {
            $(`label[for="${$(this).attr('id')}"]`).html($(this).attr('data-yes'));
            $(`#${$(this).attr('id')}-un`).prop('disabled',true);
        }
        else {
            $(`label[for="${$(this).attr('id')}"]`).html($(this).attr('data-no'));
            $(`#${$(this).attr('id')}-un`).prop('disabled',false);
        }
    })

    // When opening search modal, restore the search fields
    $("#advancedSearch").on("shown.bs.modal", function () {
        const urlParams = new URLSearchParams(window.location.search);
        for (key of urlParams.keys()) {
            if(key.startsWith('search-')) {
                if($(`.toggleSearch[data-toggle="${key}"]`).length > 0) {
                    $("#"+key).val(urlParams.getAll(key));
                    $("#"+key).trigger('change');
                    $(`.toggleSearch[data-toggle="${key}"]`)[0].checked = true;
                    // $(`.toggleSearch[data-toggle="${key}"]`).first().trigger('change');
                }
                else if($(`.toggleSearch-select[data-toggle="${key}"]`).length > 0) {
                    $("#"+key).selectpicker('val',urlParams.getAll(key));
                    $("#"+key).selectpicker('refresh');
                    $("#"+key).trigger('change');
                    $(`.toggleSearch-select[data-toggle="${key}"]`)[0].checked = true;
                    // $(`.toggleSearch-select[data-toggle="${key}"]`).first().trigger('change');
                }
            }
        }
        $('.toggleSearch').each(function (i, obj) {
            $(this).trigger('change');
        });
        $('.toggleSearch-select').each(function (i, obj) {
            $(this).trigger('change');
        });
    });

    // Remove filter when the red button is clicked, keeping only linker
    $("#clearFilter").on("click", function () {
        console.log('CLICK')
        const urlParams = new URLSearchParams(window.location.search);
        let params = '';
        if(urlParams.has('linker')) {
            params = '?linker=' + urlParams.get('linker');
        }
        window.location.href = '/units' + params;
    });
});