<!-- src/ResultsPage.svelte -->
<script>
  export let params = {};
  console.log(params);
  let query = params.query;
  let searchResults = [];
  function performSearch() {
    // Perform search logic here (dummy data for illustration)
    searchResults = ["Result 1", "Result 2", "Result 3"];
  }
</script>

<div class="content">
  <section class="resultsPageSearch">
    <div class="col">
      <h2 class="searchLogo">Stocks Guru</h2>
      <div class="search">
        <input
          class="searchInput"
          type="text"
          bind:value={query}
          placeholder="Search results..."
        />
        <button class="searchButton" on:click={performSearch}>Search</button>
      </div>
    </div>
  </section>

  <section>
    <h2>Search Results</h2>
    {#if searchResults.length > 0}
      {#each searchResults as result (result)}
        <p>{result}</p>
      {/each}
    {:else}
      <p>No results found.</p>
    {/if}
  </section>
</div>

<style>
  .content {
    width: 100%;
    margin: 2rem;
  }
  div.col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1rem;
  }
  section.resultsPageSearch {
    margin-bottom: 5rem;
  }

  h2.searchLogo {
    font-weight: 700;
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 0;
    padding-left: 0.5rem;
    text-align: start;
  } 
</style>
