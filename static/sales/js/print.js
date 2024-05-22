document.addEventListener('DOMContentLoaded', function() {
    // Función para imprimir el contenido del modal
    function printModalContent() {
        var content = document.querySelector('.modal-body').innerText; // Captura el texto del modal
        var printWindow = window.open('', '_blank'); // Abre una nueva ventana
        printWindow.document.write('<html><head><title>Impresión</title></head><body>'); // Escribe el encabezado HTML básico
        printWindow.document.write(content); // Escribe el contenido del modal
        printWindow.document.write('</body></html>'); // Cierra el cuerpo y el documento
        printWindow.document.close(); // Cierra el documento
        printWindow.print(); // Abre la ventana de impresión
        console.log("imprimir")
    }

    // Ejemplo de uso: Imprimir cuando se hace clic en un botón
    document.getElementById('printButton').addEventListener('click', printModalContent);
});