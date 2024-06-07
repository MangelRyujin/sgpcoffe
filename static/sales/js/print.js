document.addEventListener('DOMContentLoaded', function() {

    function printModalContent() {
        
        var content = document.querySelector('.modal-body').innerHTML;

       
        var printWindow = window.open('', '_blank');

        printWindow.document.write('<html><head><title>Impresión</title>');
        printWindow.document.write('<style>' +
            '#contentContainer {width: 100%; margin: 0 auto; text-align: center;}' + 
            '#contentContainer table {display: block;width: 100%; margin-left: auto; margin-right: auto; text-align: left;}' + 
            '#contentContainer.center {position: relative; left: 50%; top: 50%; transform: translate(-50%, -50%);}' + 
            
            '</style>');
        printWindow.document.write('</head><body>');

        printWindow.document.write('<div id="contentContainer">' + "Rueda de la fortuna" + '</div>');
        printWindow.document.write('<div id="contentContainer">' + "Gracias por escogernos" + '</div>');
        printWindow.document.write('<div id="contentContainer">' + content + '</div>');

        printWindow.document.write('</body></html>');

        printWindow.document.close();

        printWindow.print();
    }

    
    document.getElementById('printButton').addEventListener('click', printModalContent);
});