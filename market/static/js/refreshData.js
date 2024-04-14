

function refreshData() {
    $.ajax({
        type: "GET",
        url: "/get_company_data",
        success: function(data) {
            // Update the table with the latest data
            $("#company-table").html(data);
        }
    });
}

$(document).ready(function() {
    setInterval(refreshData, 5000); // Refresh data every 5 seconds
});
