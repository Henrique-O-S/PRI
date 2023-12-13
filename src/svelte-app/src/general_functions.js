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


export async function getArticleCompanies(id) {
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
    if (dateStr === "") {
        return "";
    }
    let date = new Date(dateStr);
    return date.toISOString().replace('T', ' ').slice(0, 19);
}

export function fixArticleText(text) {
    text = text.split(/\. (?=[A-Z])/);
    let paragraphs = [];

    // Check if the first paragraph has "letter:letter" and split it
    if (text[0].includes(":")) {
        const splitText = text[0].split(":");
        paragraphs.push(splitText[0] + ":");
        paragraphs.push(splitText[1]);
    } else {
        paragraphs.push(text[0] + ".");
    }

    let currParagraph = paragraphs.length - 1;
    for (let i = 1; i < text.length; i++) {
        if (text[i].indexOf(" - ") !== -1) {
            currParagraph++;
            paragraphs.push(text[i] + ".");
        } else {
            paragraphs[currParagraph] += text[i] + ".";
        }
    }

    return paragraphs;
}


