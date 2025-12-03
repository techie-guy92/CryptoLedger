(function ($) {
    $(document).ready(function () {
        function fetchLivePrices() {
            fetch("/main/fetch-prices/")
                .then(response => response.json())
                .then(data => {
                    $(".live-coin-price").each(function () {
                        const coin = $(this).data("coin").toUpperCase();
                        if (data[coin]) {
                            $(this).text(`$${data[coin]}`);
                        } else {
                            $(this).text("N/A");
                        }
                    });
                })
                .catch(err => {
                    console.error("Error fetching live prices:", err);
                });
        }

        fetchLivePrices();

        setInterval(fetchLivePrices, 30000);
    });
})(django.jQuery);