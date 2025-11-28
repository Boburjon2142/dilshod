document.addEventListener("DOMContentLoaded", () => {
    const deleteLinks = document.querySelectorAll(".js-delete-link");
    deleteLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const message = link.dataset.confirm || "Mahsulotni o‘chirasizmi?";
            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Optional client-side filter to narrow down the currently shown table rows.
    const filterInput = document.querySelector("[data-filter-table]");
    if (filterInput) {
        const rowSelector = filterInput.dataset.filterRows || "#productTable tbody tr";
        const rows = () => Array.from(document.querySelectorAll(rowSelector));
        filterInput.addEventListener("input", () => {
            const term = filterInput.value.trim().toLowerCase();
            rows().forEach((row) => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(term) ? "" : "none";
            });
        });
    }

});
