$(document).ready(function() {
  $.ajax({
    url: "/reportes/estadisticas/anual/options/list/",
    type: "GET",
    dataType: "json",
    success: (jsonResponse) => {
      // Load all the options
      jsonResponse.options.forEach(option => {
        $("#year").append(new Option(option, option));
      });
      jsonResponse.products.forEach(name => {
        $("#product").append(new Option(name, name));
      });
      jsonResponse.products.forEach(name => {
        $("#product2").append(new Option(name, name));
      });
      jsonResponse.products.forEach(name => {
        $("#product3").append(new Option(name, name));
      });
      // Load data for the first option
      loadAllCharts($("#year").children().first().val(),$("#product").children().first().val(),$("#product2").children().first().val(),$("#product3").children().first().val());
    },
    error: () => console.log("Failed to fetch chart filter options!")
  });
});



$("#filterForm").on("submit", (event) => {
  event.preventDefault();

  const year = $("#year").val();
  const product = $("#product").val();
  const product2 = $("#product2").val();
  const product3 = $("#product3").val();
  loadAllCharts(year,product,product2,product3)
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
      chart.data.labels =labels;
      datasets.forEach(dataset => {
        chart.data.datasets.push(dataset);
      });
      chart.update();
    },
    error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
  });
}

function loadAllCharts(year,product,product2,product3) {
  loadChart(salesChart, `/reportes/estadisticas/anual/sales/${year}/${product}/${product2}/${product3}/`);
  loadChart(spendPerCustomerChart, `/reportes/estadisticas/anual/sales/spend-per-customer/${year}/${product}/${product2}/${product3}/`);
  loadChart(paymentSuccessChart, `/reportes/estadisticas/anual/sales/payment-success/${year}/${product}/${product2}/${product3}/`);
  loadChart(salesChartPrice, `/reportes/estadisticas/anual/sales/price/${year}/${product}/${product2}/${product3}/`);
  loadChart(spendPerCustomerChartPrice, `/reportes/estadisticas/anual/sales/price/spend-per-customer/${year}/${product}/${product2}/${product3}/`);
  loadChart(paymentSuccessChartPrice, `/reportes/estadisticas/anual/sales/price/payment-success/${year}/${product}/${product2}/${product3}/`);
}