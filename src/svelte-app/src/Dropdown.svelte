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
  {#each filteredSearches as query (query)}
    <div on:click={() => handleRecentSearchClick(query.query)}>{query.query}</div>
  {/each}
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