export async function getSuggestions(input) {
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

export async function getQuery(input, category = "", fromDate = "", toDate = "") {
    console.log("Input: ", input, "Category: ", category, "From: ", fromDate, "To: ", toDate)
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            text: input,
            category: category,
            from_date: fromDate,
            to_date: toDate 
        })
    };

    console.log("Request options: ", requestOptions.body)

    try {
    const response = await fetch('http://localhost:8001/user_query', requestOptions);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
        return await response.json().then(data => data.response);
    } catch (error) {
        console.error('Error fetching query response:', error);
        return [];
    }
}


export async function getQuery(id) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            id: id
        })
    };

    try {
    const response = await fetch('http://localhost:8001/article_companies', requestOptions);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
        return await response.json().then(data => data.response);
    } catch (error) {
        console.error('Error fetching query response:', error);
        return [];
    }
}

export function convertDateString(dateStr) {
    let date = new Date(dateStr);
    return date.toISOString().replace('T', ' ').slice(0, 19);
}

