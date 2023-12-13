<!-- src/Result.svelte -->
<script>
    export let result = {};
    import { convertDateString } from "./general_functions.js";
    import { push } from "svelte-spa-router";
</script>

<div class="result">
    <div class="result-header">
        <img src="/img/cnbc.png" alt={"cbnc.logo"} />
        <span
            on:click={() => {
                push(`/article/${result.id}`);
            }}
            class="link">{result.article_title}</span
        >
    </div>
    <div class="result-content">
        <p>
            <small>{convertDateString(result.article_date)} -</small>
            {result.article_text.slice(0, 200)}...
        </p>
    </div>
</div>

<style>
    span,
    p {
        text-align: left;
        width: fit-content;
    }

    p {
        font-weight: 500;
        text-align: justify;
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
        font-size: 1.3rem;
        font-weight: 600;
    }

    .link:hover {
        text-decoration: underline;
        cursor: pointer;
    }

    small{
        opacity: 0.4;
        font-weight: 600;
    }
</style>
