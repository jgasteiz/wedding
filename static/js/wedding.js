(function () {
    'use_strict';

    $('.js-open-modal').click(function (e) {
        e.preventDefault();
        var imgSrc = $(e.currentTarget).data('img');

        var $modal = $('<div>').addClass('modal'),
            $img = $('<img>').prop('src', imgSrc),
            $modalClose = $('<div>').addClass('modal__close');

        $modal.append($img);
        $modal.append($modalClose);
        $(document.body).addClass('modal--open');
        $(document.body).append($modal);

        $modal.click(function (e) {
            $(document.body).removeClass('modal--open');
            $modal.remove();
        });
        $modalClose.click(function (e) {
            $(document.body).removeClass('modal--open');
            $modal.remove();
        });
    });

})();