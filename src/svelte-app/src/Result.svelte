<!-- src/Result.svelte -->
<script>
    export let result = {};
    console.log(result);
</script>

<div class="result">
    <div class="result-header">
        <img src={result.icon} alt={result.companyName} />
        <div class="company-info">
            <h3>{result.companyName}</h3>
            <p>{result.url}</p>
        </div>
    </div>
    <div class="result-content">
        <h2>{result.title}</h2>
        <p>{result.description}</p>
    </div>
</div>

<style>
    h3, h2{
        text-align: left;
    }
    .result {
        border: 1px solid #ccc;
        padding: 1rem;
        margin: 1rem 0;
        display: flex;
        flex-direction: column;
    }

    .result-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }

    .company-info {
        margin-left: 1rem;
    }

    img {
        width: 50px; /* Adjust the size based on your design */
        height: 50px; /* Adjust the size based on your design */
    }

    .result-content {
        margin-top: 0.5rem;
    }
</style>
