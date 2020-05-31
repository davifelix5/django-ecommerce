(function () {
    variations_form = document.getElementById('select-variacoes');
    original_price = document.getElementById('variation-preco');
    promotional_price = document.getElementById('variation-preco-promocional');

    if (!variations_form) {
        return;
    }

    if (!original_price) {
        return;
    }

    variations_form.addEventListener('change', function () {
        preco = this.options[this.selectedIndex].getAttribute('original-price');
        preco_promocional = this.options[this.selectedIndex].getAttribute('promotional-price');

        original_price.innerHTML = preco;

        if (preco_promocional != "null") {
            original_price.classList = 'lead product-old-price text-muted';
            promotional_price.innerHTML = preco_promocional;
        }
        if (preco_promocional == "null") {
            promotional_price.innerHTML = ""
            original_price.classList = 'lead product-price';
        }
    })
})();

