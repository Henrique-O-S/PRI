<!-- src/ResultsPage.svelte -->
<script>
  import { push } from "svelte-spa-router";
  import Category from "./Category.svelte";
  import Company from "./Company.svelte";
  import DateFilter from "./DateFilter.svelte";
  import Result from "./Result.svelte";
  import SearchBar from "./SearchBar.svelte";
  import {getCompanyResults, getSearchResults} from "./mockdata.js"
  import { getQuery } from './general_functions.js'
  export let params = {};
  console.log(params);
  let selectedQuery;
  let searchResults;
  let companies;
  let company;
  let company_index = 0;
  let results;
  $: {
    selectedQuery = params.query;
    console.log('GOT THIS QUERY: ', selectedQuery)
    searchResults = getSearchResults();
    companies = getCompanyResults();
    company = companies[company_index];
    results = getResults(selectedQuery);
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

  async function getResults(query) {
    try {
      results = await getQuery(query);
      console.log(results);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  }

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
