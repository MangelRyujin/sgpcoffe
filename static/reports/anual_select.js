$(document).ready(function() {
  $.ajax({
    url: "/ventas/chart/filter-options/",
    type: "GET",
    dataType: "json",
    success: (jsonResponse) => {
      // Load all the options
      jsonResponse.options.forEach(option => {
        $("#year").append(new Option(option, option));
      });
      // Load data for the first option
      loadAllCharts($("#year").children().first().val());
    },
    error: () => console.log("Failed to fetch chart filter options!")
  });
});

$("#filterForm").on("submit", (event) => {
  event.preventDefault();

  const year = $("#year").val();
  loadAllCharts(year)
});

function loadChart(chart, endpoint) {
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

function loadAllCharts(year) {
  loadChart(salesChart, `/ventas/chart/sales/${year}/`);
  loadChart(spendPerCustomerChart, `/ventas/chart/spend-per-customer/${year}/`);
  loadChart(paymentSuccessChart, `/ventas/chart/payment-success/${year}/`);
}