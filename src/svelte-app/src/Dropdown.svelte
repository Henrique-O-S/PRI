<!-- src/Dropdown.svelte -->
<script>
  export let performSearch = "";
  let predefinedQueries = [
    { query: "Tesla dipped" },
    { query: "advanced micron devices" },
    { query: "cyber security stocks" },
  ];

  export let selectedQuery = "";
  export let suggestions = [];
  export let isEmpty = true;

  function handleRecentSearchClick(query) {
    selectedQuery = query;
    performSearch(selectedQuery);
  }
</script>

<div class="dropdown">
  {#if isEmpty}
    {#each predefinedQueries as search}
      <div on:click={() => handleRecentSearchClick(search.query)}>
        {search.query}
      </div>
    {/each}
  {:else}
    {#each suggestions as suggestion}
      <div on:click={() => handleRecentSearchClick(suggestion)}>
        {suggestion}
      </div>
    {/each}
  {/if}
</div>

<style>
  .dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 1;
    display: flex;
    flex-direction: column;
  }

  .dropdown div {
    padding: 0.5rem;
    cursor: pointer;
  }
</style>
