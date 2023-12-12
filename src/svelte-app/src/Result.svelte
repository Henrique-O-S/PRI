<!-- src/Result.svelte -->
<script>
    export let result = {};
    console.log(result);
</script>

<div class="result">
    <div class="result-header">
        <img src="/img/cnbc.png" alt={result.companyName} />
        <div class="company-info">
            <h3>{result.companyName}</h3>
            <p>{result.url}</p>
        </div>
    </div>
    <div class="result-content">
        <a href={result.url} class="link">{result.title}</a>
        <p>{result.description}</p>
    </div>
</div>

<style>
    h3,
    a,
    p {
        text-align: left;
        width: fit-content;
    }
    .result-content a {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0;
    }
    p {
        font-weight: 500;
    }
    .result {
        border-bottom: 1px solid #dedada;
        padding: 1rem;
        margin: 0;
        display: flex;
        flex-direction: column;
    }

    .result-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.2rem;
        gap: 1rem;
    }

    .company-info h3 {
        font-size: 1.3rem;
    }

    .company-info p {
        font-size: 1rem;
    }

    .result-header * {
        margin: 0;
    }

    img {
        width: 40px; /* Adjust the size based on your design */
        height: 40px; /* Adjust the size based on your design */
    }

    .result-content {
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .link {
        color: rgb(81, 81, 225);
        margin-bottom: 0.5rem;
        font-size: 1.4rem;
    }

    .link:hover {
        text-decoration: underline;
        cursor: pointer;
    }
</style>
