<!-- src/Category.svelte -->
<script>
    export let category;
    export let selectCategory;
</script>

{#if category.selected}
    <div class="tag selected" on:click={() => selectCategory(category)}>
        {category.name}
    </div>
{:else}
    <div class="tag" on:click={() => selectCategory(category)}>
        {category.name}
    </div>
{/if}

<style>
    .tag {
        display: inline-block;
        background-color: white;
        padding: 0.8rem 1.2rem 0.8rem 1.2rem;
        border-radius: 20px;
        border: 1px solid #dedada;
        cursor: pointer;
        display: flex;
        align-items: center;
        box-sizing: border-box;
        font-size: 0.85rem;
    }
    .tag.selected {
        background-color: darkgray;
        border: 1px solid black;;
        color: white;
    }
</style>
