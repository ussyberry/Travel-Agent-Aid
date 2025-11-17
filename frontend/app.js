document.addEventListener('DOMContentLoaded', () => {

    // Flight Search
    const flightForm = document.getElementById('flight-search-form');
    if (flightForm) {
        flightForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const form = event.target;
            const origin = form.origin.value;
            const destination = form.destination.value;
            const departure_date = form.departure_date.value;
            const adults = form.adults.value;
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = 'Searching for flights...';
            const url = `/api/flights?origin=${origin}&destination=${destination}&departure_date=${departure_date}&adults=${adults}`;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = '';
                    if (data.error) {
                        resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                    } else if (data.length === 0) {
                        resultsDiv.innerHTML = '<p>No flights found.</p>';
                    } else {
                        const flights = data.map(flight => {
                            return `
                                <div>
                                    <p><strong>Price:</strong> ${flight.price.total} ${flight.price.currency}</p>
                                    <p><strong>Airlines:</strong> ${flight.itineraries[0].segments.map(segment => segment.carrierCode).join(', ')}</p>
                                </div>
                            `;
                        }).join('');
                        resultsDiv.innerHTML = flights;
                    }
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<p>Error: ${error}</p>`;
                });
        });
    }

    // Visa Requirements
    const visaForm = document.getElementById('visa-search-form');
    if (visaForm) {
        visaForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const form = event.target;
            const origin = form['visa-origin'].value;
            const destination = form['visa-destination'].value;
            const nationality = form['visa-nationality'].value;
            const resultsDiv = document.getElementById('visa-results');
            resultsDiv.innerHTML = 'Checking visa requirements...';
            fetch(`/api/visa-requirements?origin=${origin}&destination=${destination}&nationality=${nationality}`)
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<p>Error: ${error}</p>`;
                });
        });
    }

    // Nearest Airports
    const airportForm = document.getElementById('nearest-airport-form');
    if (airportForm) {
        airportForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const form = event.target;
            const keyword = form.keyword.value;
            const resultsDiv = document.getElementById('airport-results');
            resultsDiv.innerHTML = 'Searching for nearest airports...';
            const url = `/api/nearest-airports?keyword=${keyword}`;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = '';
                    if (data.error) {
                        resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                    } else if (data.length === 0) {
                        resultsDiv.innerHTML = '<p>No airports found.</p>';
                    } else {
                        const airports = data.map(airport => {
                            return `
                                <div>
                                    <p><strong>Name:</strong> ${airport.name}</p>
                                    <p><strong>IATA Code:</strong> ${airport.iataCode}</p>
                                    <p><strong>Distance:</strong> ${airport.distance.value} ${airport.distance.unit}</p>
                                </div>
                            `;
                        }).join('');
                        resultsDiv.innerHTML = airports;
                    }
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<p>Error: ${error}</p>`;
                });
        });
    }

    // Hotel Search
    const hotelForm = document.getElementById('hotel-search-form');
    if (hotelForm) {
        hotelForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const cityCode = event.target['city-code'].value;
            const resultsDiv = document.getElementById('hotel-results');
            resultsDiv.innerHTML = 'Searching for hotels...';
            fetch(`/api/hotels?city_code=${cityCode}`)
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<p>Error: ${error}</p>`;
                });
        });
    }

    // Activity Search
    const activityForm = document.getElementById('activity-search-form');
    if (activityForm) {
        activityForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const keyword = event.target.keyword.value;
            const resultsDiv = document.getElementById('activity-results');
            resultsDiv.innerHTML = 'Searching for activities...';
            fetch(`/api/activities?keyword=${keyword}`)
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<p>Error: ${error}</p>`;
                });
        });
    }
});
