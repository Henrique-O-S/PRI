<!-- src/ResultsPage.svelte -->
<script>
  import Category from "./Category.svelte";
  import DateFilter from "./DateFilter.svelte";
  import Result from "./Result.svelte";
  import SearchBar from "./SearchBar.svelte";
  export let params = {};
  console.log(params);
  let selectedQuery;
  let searchResults;
  let showDates = false;
  $: {
    selectedQuery = params.query;
    searchResults = [
      {
        companyName: "Facebook",
        url: "https://www.facebook.com/tools/ads-manager",
        title: "Ads Manager",
        description:
          "Ads Manager is your starting point for running ads on Facebook, Instagram, Messenger, or Audience Network. It's an all-in-one tool for creating ads.",
      },
      {
        icon: "path/to/facebook-icon.png",
        companyName: "Facebook",
        url: "https://www.facebook.com/tools/ads-manager",
        title: "Ads Manager",
        description:
          "Ads Manager is your starting point for running ads on Facebook, Instagram, Messenger, or Audience Network. It's an all-in-one tool for creating ads.",
      },
      {
        icon: "path/to/facebook-icon.png",
        companyName: "Facebook",
        url: "https://www.facebook.com/tools/ads-manager",
        title: "Ads Manager",
        description:
          "Ads Manager is your starting point for running ads on Facebook, Instagram, Messenger, or Audience Network. It's an all-in-one tool for creating ads.",
      },
      {
        icon: "path/to/facebook-icon.png",
        companyName: "Facebook",
        url: "https://www.facebook.com/tools/ads-manager",
        title: "Ads Manager",
        description:
          "Ads Manager is your starting point for running ads on Facebook, Instagram, Messenger, or Audience Network. It's an all-in-one tool for creating ads.",
      },
      {
        icon: "path/to/facebook-icon.png",
        companyName: "Facebook",
        url: "https://www.facebook.com/tools/ads-manager",
        title: "Ads Manager",
        description:
          "Ads Manager is your starting point for running ads on Facebook, Instagram, Messenger, or Audience Network. It's an all-in-one tool for creating ads.",
      },
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
  let padding = "0.6rem";
  let time = 0.28;
  let categories = [
    { name: "All", selected: false },
    { name: "News", selected: false },
    { name: "Images", selected: false },
    { name: "Videos", selected: false },
    { name: "Maps", selected: false },
    { name: "Shopping", selected: false },
  ];
  function selectCategory(category) {
    category.selected = !category.selected;
    categories = [...categories];
  }
  function applyFilter(startDate, endDate) {
    console.log(startDate, endDate);
  }
</script>

<div class="content">
  <section class="resultsPageSearch">
    <div class="col">
      <h2 class="searchLogo">Stocks Guru</h2>
      <SearchBar {selectedQuery} {width} {padding} />
      <div class="row" style="gap: 0.5rem;">
        {#each categories as category}
          <Category {category} {selectCategory} />
        {/each}
        <div class="col" style="gap: 0rem; flex:1">
          <span on:click={() => (showDates = !showDates)}>Filter by date</span>
          {#if showDates}
            <DateFilter {applyFilter} />
          {/if}
        </div>
      </div>
    </div>
  </section>
  <hr />
  <div class="row" style="gap:5rem;">
    <section class="results">
      <h5 class="time">{searchResults.length} Results in {time} seconds</h5>
      {#if searchResults.length > 0}
        {#each searchResults as result}
          <Result {result} />
        {/each}
      {:else}
        <p>No results found.</p>
      {/if}
    </section>
    <section class="companyInfo">
      <div>Company info</div>
    </section>
  </div>
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
  div.row {
    display: flex;
    flex-direction: row;
  }
  section.resultsPageSearch {
    margin-bottom: 1.2rem;
  }

  h2.searchLogo {
    font-weight: 700;
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 0;
    padding-left: 0.5rem;
    text-align: start;
  }

  section.results {
    width: 60%;
  }

  section.results h5.time {
    text-align: start;
    opacity: 0.4;
    font-size: 0.9rem;
    padding-left: 1rem;
    margin-bottom: 0.2rem;
  }

  section.companyInfo div {
    background-color: aqua;
  }
  section.companyInfo {
    flex: 1;
  }
  span {
    cursor: pointer;
  }
  hr {
    margin-bottom: 1rem;
    margin-top: 1rem;
    background-color: silver;
    height: 1.5px;
    opacity: 30%;
  }
</style>
