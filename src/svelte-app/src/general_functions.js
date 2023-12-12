async function getSuggestions(input) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input })
    };

    try {
    const response = await fetch('http://localhost:8001/suggestions', requestOptions);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
        return await response.json().then(data => data.response);
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        return [];
    }
}

