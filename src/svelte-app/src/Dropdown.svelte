<!-- src/Dropdown.svelte -->
<script>
  export let performSearch = "";

  let recentSearches = ["Apple", "Tesla", "Amazon", "Recent Search 1", "Recent Search 2"];

  let selectedQuery = "";

  function handleRecentSearchClick(query) {
    selectedQuery = query;
    performSearch(selectedQuery);
  }
</script>

<div class="dropdown">
  {#each recentSearches as query (query)}
    <div on:click={() => handleRecentSearchClick(query)}>{query}</div>
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
