<!-- src/ResultsPage.svelte -->
<script>
  import { push } from "svelte-spa-router";
  import Category from "./Category.svelte";
  import Company from "./Company.svelte";
  import DateFilter from "./DateFilter.svelte";
  import Result from "./Result.svelte";
  import SearchBar from "./SearchBar.svelte";
  export let params = {};
  console.log(params);
  let selectedQuery;
  let searchResults;
  let companies;
  let company;
  let company_index = 0;
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
    companies = [
      {
        name: "Facebook",
        tag: "FB",
        description:
          "Facebook, Inc. is an American technology conglomerate based in Menlo Park, California.",
      },
      {
        name: "Apple",
        tag: "AAPL",
        description:
          "Apple Inc. is an American multinational technology company headquartered in Cupertino, California.",
      },
      {
        name: "Amazon",
        tag: "AMZN",
        description:
          "Amazon.com, Inc. is an American multinational technology company based in Seattle, Washington.",
      },
      {
        name: "Netflix",
        tag: "NFLX",
        description:
          "Netflix, Inc. is an American over-the-top content platform and production company headquartered in Los Gatos, California.",
      },
      {
        name: "Google",
        tag: "GOOGL",
        description:
          "Google LLC is an American multinational technology company that specializes in Internet-related services and products.",
      },
      {
        name: "Microsoft",
        tag: "MSFT",
        description:
          "Microsoft Corporation is an American multinational technology company with headquarters in Redmond, Washington.",
      },
      {
        name: "Tesla",
        tag: "TSLA",
        description:
          "Tesla, Inc. is an American electric vehicle and clean energy company based in Palo Alto, California.",
      },
      {
        name: "Twitter",
        tag: "TWTR",
        description:
          "Twitter is an American microblogging and social networking service on which users post and interact with messages known as tweets.",
      },
      {
        name: "Alphabet",
        tag: "GOOGL",
        description:
          "Alphabet Inc. is an American multinational conglomerate headquartered in Mountain View, California.",
      },
      {
        name: "Intel",
        tag: "INTC",
        description:
          "Intel Corporation is an American multinational corporation and technology company headquartered in Santa Clara, California.",
      },
      {
        name: "Nvidia",
        tag: "NVDA",
        description:
          "Nvidia Corporation is an American multinational technology company incorporated in Delaware and based in Santa Clara, California.",
      },
      {
        name: "PayPal",
        tag: "PYPL",
        description:
          "PayPal Holdings, Inc. is an American company operating an online payments system in majority of countries that supports online money transfers.",
      },
      {
        name: "Adobe",
        tag: "ADBE",
        description:
          "Adobe Inc. is an American multinational computer software company headquartered in San Jose, California.",
      },
    ];
    company = companies[company_index];
  }
  let width = "50%";
  let padding = "0.6rem";
  let time = 0.28;
  let categories = [
    { name: "All", selected: true },
    { name: "cybersecurity", selected: false },
    { name: "software", selected: false },
    { name: "hardware", selected: false },
    { name: "semiconductors", selected: false },
    { name: "finance", selected: false },
  ];
  function selectCategory(category) {
    for (let category_el of categories) {
      category_el.selected = category === category_el;
    }
    categories = [...categories];
  }
  function applyFilter(startDate, endDate) {
    console.log(startDate, endDate);
  }
  function updateCompany(inc) {
    company_index += inc;
    if (company_index < 0) {
      company_index = companies.length - 1;
    } else if (company_index >= companies.length) {
      company_index = 0;
    }
  }
</script>

<div class="content">
  <section class="resultsPageSearch">
    <div class="col">
      <div class="row">
        <h2 class="searchLogo" on:click={() => push("/")}>Stocks Guru</h2>
      </div>
      <SearchBar {selectedQuery} {width} {padding} />
      <div class="row" style="gap: 0.5rem;">
        {#each categories as category}
          <Category {category} {selectCategory} />
        {/each}
        <DateFilter {applyFilter} />
      </div>
    </div>
  </section>
  <hr />
  <div class="row" style="gap:10rem; padding-right:3rem;">
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
      <Company {company} {updateCompany} />
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
    cursor: pointer;
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

  hr {
    margin-bottom: 1rem;
    margin-top: 1rem;
    background-color: silver;
    height: 1.5px;
    opacity: 30%;
  }
</style>
