<!-- src/ResultsPage.svelte -->
<script>
  export let selectedQuery = "";
  let searchResults = [];

  function performSearch() {
    // Perform search logic here (dummy data for illustration)
    searchResults = ["Result 1", "Result 2", "Result 3"];
  }
</script>

<main>
  <header>
    <h1>Results Page</h1>
  </header>

  <section class="main-page-center-section">
    <div class="row">
      <div class="control">
        <input
          class="input"
          type="text"
          bind:value={selectedQuery}
          placeholder="Search results..."
        />
        <button on:click={performSearch}>Search</button>
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
</main>

<style>
  /* Add your styling here */
</style>
