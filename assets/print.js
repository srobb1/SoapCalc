document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed'); // Debugging statement

    let observer; // Declare observer variable
    let debounceTimeout; // Timeout for debounce

    function addPrintButtonListener() {
        const printButton = document.getElementById('print-button');
        if (printButton) {
            console.log('Print button found'); // Debugging statement
            printButton.addEventListener('click', function () {
                if (debounceTimeout) {
                    clearTimeout(debounceTimeout);
                }
                debounceTimeout = setTimeout(function () {
                    console.log('Print button clicked!'); // Debugging statement
                    window.print();
                }, 300); // Debounce delay
            });
            if (observer) {
                console.log('Disconnecting observer'); // Debugging statement
                observer.disconnect(); // Disconnect the observer once the button is found
            }
        } else {
            console.log('Print button not found'); // Debugging statement
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


