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
            resultsDiv.innerHTML = '<div class="loading">Searching for flights...</div>';
            const url = `/api/flights?origin=${origin}&destination=${destination}&departure_date=${departure_date}&adults=${adults}`;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = '';
                    if (data.error) {
                        resultsDiv.innerHTML = `<div class="error">Error: ${data.error}${data.message ? '<br>' + data.message : ''}</div>`;
                    } else if (data.length === 0) {
                        resultsDiv.innerHTML = '<div class="result-item">No flights found for the specified route and date.</div>';
                    } else {
                        const flights = data.map(flight => {
                            const segments = flight.itineraries[0].segments || [];
                            const airlines = [...new Set(segments.map(segment => segment.carrierCode))].join(', ');
                            const departure = segments[0] ? `${segments[0].departure.iataCode} ${segments[0].departure.at.split('T')[1].substring(0, 5)}` : '';
                            const arrival = segments[segments.length - 1] ? `${segments[segments.length - 1].arrival.iataCode} ${segments[segments.length - 1].arrival.at.split('T')[1].substring(0, 5)}` : '';
                            
                            return `
                                <div class="flight-card">
                                    <div class="flight-price">${flight.price.total} ${flight.price.currency}</div>
                                    <div class="flight-details">
                                        ${airlines ? `<span><strong>Airlines:</strong> ${airlines}</span>` : ''}
                                        ${departure ? `<span><strong>Departure:</strong> ${departure}</span>` : ''}
                                        ${arrival ? `<span><strong>Arrival:</strong> ${arrival}</span>` : ''}
                                        ${segments.length > 1 ? `<span><strong>Stops:</strong> ${segments.length - 1}</span>` : '<span><strong>Direct</strong></span>'}
                                    </div>
                                </div>
                            `;
                        }).join('');
                        resultsDiv.innerHTML = flights;
                    }
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<div class="error">Error: ${error.message || 'Failed to fetch flights'}</div>`;
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
            resultsDiv.innerHTML = '<div class="loading">Checking visa requirements...</div>';
            fetch(`/api/visa-requirements?origin=${origin}&destination=${destination}&nationality=${nationality}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        resultsDiv.innerHTML = `<div class="error">Error: ${data.error}${data.message ? '<br>' + data.message : ''}</div>`;
                    } else {
                        resultsDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                    }
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<div class="error">Error: ${error.message || 'Failed to check visa requirements'}</div>`;
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
            resultsDiv.innerHTML = '<div class="loading">Searching for nearest airports...</div>';
            const url = `/api/nearest-airports?keyword=${keyword}`;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = '';
                    if (data.error) {
                        resultsDiv.innerHTML = `<div class="error">Error: ${data.error}${data.message ? '<br>' + data.message : ''}</div>`;
                    } else if (data.length === 0) {
                        resultsDiv.innerHTML = '<div class="result-item">No airports found near the specified location.</div>';
                    } else {
                        const airports = data.map(airport => {
                            return `
                                <div class="airport-card">
                                    <div class="airport-name">
                                        <span class="airport-code">${airport.iataCode || 'N/A'}</span>
                                        ${airport.name || 'Unknown Airport'}
                                    </div>
                                    ${airport.distance ? `<p><strong>Distance:</strong> ${airport.distance.value} ${airport.distance.unit}</p>` : ''}
                                </div>
                            `;
                        }).join('');
                        resultsDiv.innerHTML = airports;
                    }
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<div class="error">Error: ${error.message || 'Failed to find airports'}</div>`;
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
            resultsDiv.innerHTML = '<div class="loading">Searching for hotels...</div>';
            fetch(`/api/hotels?city_code=${cityCode}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        resultsDiv.innerHTML = `<div class="error">Error: ${data.error}${data.message ? '<br>' + data.message : ''}</div>`;
                    } else {
                        resultsDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                    }
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<div class="error">Error: ${error.message || 'Failed to search hotels'}</div>`;
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
            resultsDiv.innerHTML = '<div class="loading">Searching for activities...</div>';
            fetch(`/api/activities?keyword=${keyword}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        resultsDiv.innerHTML = `<div class="error">Error: ${data.error}${data.message ? '<br>' + data.message : ''}</div>`;
                    } else {
                        resultsDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                    }
                })
                .catch(error => {
                    resultsDiv.innerHTML = `<div class="error">Error: ${error.message || 'Failed to search activities'}</div>`;
                });
        });
    }
});
