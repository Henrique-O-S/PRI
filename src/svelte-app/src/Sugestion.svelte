<!-- src/Sugestion.svelte -->
<script>
    export let suggestion;
    export let searchSuggestion;
</script>

<div class="suggestionDiv" on:click={() => searchSuggestion(suggestion)}>
    <span class="icon" role="img" aria-label="Search">🔍</span>
    <span class="suggestion">{suggestion}</span>
</div>

<style>
    .suggestionDiv {
        display: inline-block;
        background-color: white;
        padding: 0.8rem 1.2rem 0.8rem 1.2rem;
        border-radius: 20px;
        border: 1px solid #dedada;
        cursor: pointer;
        display: flex;
        align-items: center;
        box-sizing: border-box;
        font-size: 1rem;
        width: 500px;
        position: relative;
    }

    .suggestionDiv:hover {
        background-color: #f5f5f5;
    }

    .icon {
        margin-right: 0.5rem;
        transition: transform 0.3s ease; /* Animation duration and easing */
    }

    .suggestionDiv:hover .icon {
        transform: scale(1.4); /* Scale factor on hover */
    }

    .suggestion {
        flex: 1;
        font-weight: 500;
    }
</style>
