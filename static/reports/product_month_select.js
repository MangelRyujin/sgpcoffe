$(document).ready(function() {
  $.ajax({
    url: "/reportes/estadisticas/month/options/list/",
    type: "GET",
    dataType: "json",
    success: (jsonResponse) => {
      // Load all the options
      jsonResponse.options.forEach(option => {
        $("#month").append(new Option(option, option));
      });
      jsonResponse.products_month.forEach(name => {
        $("#monthproduct").append(new Option(name, name));
      });
      jsonResponse.products_month.forEach(name => {
        $("#monthproduct2").append(new Option(name, name));
      });
      jsonResponse.products_month.forEach(name => {
        $("#monthproduct3").append(new Option(name, name));
      });
      // Load data for the first option
      loadAllChartsMonth($("#month").children().first().val(),$("#monthYear").children().first().val(),$("#monthproduct").children().first().val(),$("#monthproduct2").children().first().val(),$("#monthproduct3").children().first().val());
    },
    error: () => console.log("Failed to fetch chart filter options!")
  });
});

$("#monthFilterForm").on("submit", (event) => {
  event.preventDefault();

  const month = $("#month").val();
  const monthYear = $("#monthYear").val();
  const monthproduct = $("#monthproduct").val();
  const monthproduct2 = $("#monthproduct2").val();
  const monthproduct3 = $("#monthproduct3").val();
  loadAllChartsMonth(month,monthYear,monthproduct,monthproduct2,monthproduct3)
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

function loadAllChartsMonth(month,monthYear,monthproduct,monthproduct2,monthproduct3) {
  loadChartMonth(monthSalesChart, `/reportes/estadisticas/day/sales/${month}/${monthYear}/${monthproduct}/${monthproduct2}/${monthproduct3}/`);
  loadChartMonth(monthSpendPerCustomerChart, `/reportes/estadisticas/month/spend-per-customer/${month}/${monthYear}/${monthproduct}/${monthproduct2}/${monthproduct3}/`);
  loadChartMonth(monthPaymentSuccessChart, `/reportes/estadisticas/month/payment-success/${month}/${monthYear}/${monthproduct}/${monthproduct2}/${monthproduct3}/`);
  loadChartMonth(monthSalesChartPrice, `/reportes/estadisticas/day/price/sales/${month}/${monthYear}/${monthproduct}/${monthproduct2}/${monthproduct3}/`);
  loadChartMonth(monthSpendPerCustomerChartPrice, `/reportes/estadisticas/month/price/spend-per-customer/${month}/${monthYear}/${monthproduct}/${monthproduct2}/${monthproduct3}/`);
  loadChartMonth(monthPaymentSuccessChartPrice, `/reportes/estadisticas/month/price/payment-success/${month}/${monthYear}/${monthproduct}/${monthproduct2}/${monthproduct3}/`);
}