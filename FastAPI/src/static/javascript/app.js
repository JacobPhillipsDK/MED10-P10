document.addEventListener('DOMContentLoaded', function() {
    const runButton = document.getElementById('run-button');
    runButton.addEventListener('click', get_start_and_goal);

    function get_start_and_goal() {
        const startPos = document.getElementById('startPos').value;
        const endPos = document.getElementById('endPos').value;

        console.log('Button clicked!');
        console.log(startPos);
        console.log(endPos);

        // Construct URL with parameters
        const url = `http://localhost/api/get_path?startPos=${encodeURIComponent(startPos)}&endPos=${encodeURIComponent(endPos)}`;

        console.log(url);

        send_http_request(url);
    }

    function send_http_request(url) {
        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle response data
            console.log('Response from server:', data);
            // You can further process the data here, such as updating the UI
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
    }
});
