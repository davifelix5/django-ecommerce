(function () {
    console.log('salve')
    const backupAdresses = document.querySelectorAll('.backupAddress')
    const select = document.querySelector('#changeAddress')
    const submitButton = document.querySelector('#submitChangeAddress')

    select.addEventListener('change', function () {
        const selectedAddress = this.options[this.selectedIndex].value
        
        if (isNaN(selectedAddress)) {
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
