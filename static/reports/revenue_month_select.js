$(document).ready(function() {
  $.ajax({
    url: "/ventas/chart/month/filter-options/",
    type: "GET",
    dataType: "json",
    success: (jsonResponse) => {
      // Load all the options
      jsonResponse.options.forEach(option => {
        $("#month").append(new Option(option, option));
        $("#monthYear").append(new Option(option, option));
      });
      // Load data for the first option
      loadAllChartsMonth($("#month").children().first().val(),$("#monthYear").children().first().val());
    },
    error: () => console.log("Failed to fetch chart filter options!")
  });
});

$("#monthFilterForm").on("submit", (event) => {
  event.preventDefault();

  const month = $("#month").val();
  const monthYear = $("#monthYear").val();
  loadAllChartsMonth(month,monthYear)
});

function loadChartMonth(chart, endpoint) {
  $.ajax({
    url: endpoint,
    type: "GET",
    dataType: "json",
    success: (jsonResponse) => {
      // Extract data from the response
      const title = jsonResponse.title;
      const labels = jsonResponse.data.labels;
      const datasets = jsonResponse.data.datasets;

      // Reset the current chart
      chart.data.datasets = [];
      chart.data.labels = [];

      // Load new data into the chart
      chart.options.title.text = title;
      chart.options.title.display = true;
      chart.data.labels = labels;
      datasets.forEach(dataset => {
        chart.data.datasets.push(dataset);
      });
      chart.update();
    },
    error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
  });
}

function loadAllChartsMonth(month,monthYear) {
  loadChartMonth(monthSalesChart, `/ventas/chart/revenue/day/sales/${month}/${monthYear}/`);
  loadChartMonth(monthSpendPerCustomerChart, `/ventas/chart/revenue/month/spend-per-customer/${month}/${monthYear}/`);
  loadChartMonth(monthPaymentSuccessChart, `/ventas/chart/month/payment-success/${month}/${monthYear}/`);
}