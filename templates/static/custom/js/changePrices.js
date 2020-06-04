(function () {
    variations_form = document.getElementById('select_variations');
    prices_area = document.querySelector('.prices');

    variations_form.addEventListener('change', function () {
        prices_area.innerHTML = '';
        price = this.options[this.selectedIndex].getAttribute('original-price');
        promotional_price = this.options[this.selectedIndex].getAttribute('promotional-price');

        normal_price = document.createElement('span');
        normal_price.innerHTML = price;

        if (promotional_price !== "null") {
            promo = document.createElement('span');
            promo.innerHTML = promotional_price;
            promo.classList = 'lead product-price mr-1';

            normal_price.classList = 'lead product-old-price text-muted';
            prices_area.appendChild(promo);

        } else {
            normal_price.classList = 'lead product-price';
        }

        prices_area.appendChild(normal_price);
    })
})();