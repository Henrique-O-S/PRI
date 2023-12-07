<!-- src/ResultsPage.svelte -->
<script>
  import Result from "./Result.svelte";
  import SearchBar from "./SearchBar.svelte";
  export let params = {};
  console.log(params);
  let selectedQuery;
  let searchResults;
  $: {
    selectedQuery = params.query;
    searchResults = [
      {
        icon: "path/to/facebook-icon.png",
        companyName: "Facebook",
        url: "https://www.facebook.com/tools/ads-manager",
        title: "Ads Manager",
        description:
          "Ads Manager is your starting point for running ads on Facebook, Instagram, Messenger, or Audience Network. It's an all-in-one tool for creating ads.",
      },
      // Add more result objects as needed
    ];
  }
  let width = "50%";
</script>

<div class="content">
  <section class="resultsPageSearch">
    <div class="col">
      <h2 class="searchLogo">Stocks Guru</h2>
      <SearchBar {selectedQuery} {width} />
    </div>
  </section>

  <section>
    <h2>Search Results for {selectedQuery}</h2>
    {#if searchResults.length > 0}
      {#each searchResults as result}
        <Result {result} />
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
