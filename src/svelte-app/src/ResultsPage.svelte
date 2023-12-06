<!-- src/ResultsPage.svelte -->
<script>
  import SearchBar from "./SearchBar.svelte";
  export let params = {};
  console.log(params);
  let searchResults = [];
  $: selectedQuery = params.query;
  let width = "70%";
  function performSearch() {
    // Perform search logic here (dummy data for illustration)
    searchResults = ["Result 1", "Result 2", "Result 3"];
  }
</script>

<div class="content">
  <section class="resultsPageSearch">
    <div class="col">
      <h2 class="searchLogo">Stocks Guru</h2>
      <SearchBar {selectedQuery} {width}/>
    </div>
  </section>

  <section>
    <h2>Search Results for {selectedQuery}</h2>
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
