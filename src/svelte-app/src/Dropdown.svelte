<!-- src/Dropdown.svelte -->
<script>
  export let performSearch = "";
  let recentSearches = [
    { query: "Apple" },
    { query: "Tesla" },
    { query: "Amazon" },
    { query: "Recent Search 1" },
    { query: "Recent Search 2" },
  ];
  export let selectedQuery = "";
  export let suggestions = [];
  export let isEmpty = true;

  function handleRecentSearchClick(query) {
    selectedQuery = query;
    performSearch(selectedQuery);
  }

  // Add computed property for filtered searches
  $: filteredSearches = recentSearches.filter(({ query }) =>
    query.toLowerCase().includes(selectedQuery.toLowerCase())
  );
</script>

<div class="dropdown">
  {#if isEmpty}
    {#each recentSearches as search}
      <div on:click={() => handleRecentSearchClick(search.query)}>{search.query}</div>
    {/each}
  {:else}
    {#each suggestions as suggestion}
      <div on:click={() => handleRecentSearchClick(suggestion)}>{suggestion}</div>
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