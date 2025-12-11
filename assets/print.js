document.addEventListener('DOMContentLoaded', function () {
    let observer; // Declare observer variable
    let debounceTimeout; // Timeout for debounce

    function addPrintButtonListener() {
        const printButton = document.getElementById('print-button');
        if (printButton) {
            printButton.addEventListener('click', function () {
                if (debounceTimeout) {
                    clearTimeout(debounceTimeout);
                }
                debounceTimeout = setTimeout(function () {
                    window.print();
                }, 300); // Debounce delay
            });
            if (observer) {
                observer.disconnect(); // Disconnect the observer once the button is found
            }
        }
    }

    // Try to add the listener in case the button is already in the DOM
    addPrintButtonListener();

    // Observe changes to the DOM to handle dynamically added elements
    observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.addedNodes.length > 0) {
                addPrintButtonListener();
            }
        });
    });

    const config = { childList: true, subtree: true };
    observer.observe(document.body, config);
});


