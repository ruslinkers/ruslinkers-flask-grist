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

    var $container = $('#sidebar'),
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
        console.log(target);
        if (this.checked) {
            target.removeAttr('disabled');
        }
        else {
            target.attr('disabled', 'true');
        }
    });

    // When opening search modal, restore the search fields
    $("#advancedSearch").on("shown.bs.modal", function () {
        const urlParams = new URLSearchParams(window.location.search);
        for (const [key, value] of urlParams) {
            if (key.startsWith('search-')) {
                $("#"+key).val(value);
                $(`.toggleSearch[data-toggle="${key}"]`)[0].checked = true;
                $(`.toggleSearch[data-toggle="${key}"]`).first().trigger('change');
            }
        }
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