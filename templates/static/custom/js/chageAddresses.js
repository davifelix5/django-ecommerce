(function () {
    console.log('salve')
    let backupAdresses = document.querySelectorAll('.backupAddress')
    let select = document.querySelector('#changeAddress')
    let submitButton = document.querySelector('#submitChangeAddress')

    select.addEventListener('change', function () {
        let selectedAddress = this.options[this.selectedIndex].value
        if (selectedAddress.length > 1) {
            submitButton.classList.add('hidden')
        } else {
            submitButton.classList.remove('hidden')
        }
        backupAdresses.forEach(item => {
            item.classList.add('hidden')
        })
        backupAdresses.forEach(item => {
            if (item.getAttribute('address') == selectedAddress) {
                item.classList.remove('hidden')
            }
        })
    })
})();
