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
  let searchResults = [];
  let companies;
  let company;
  let company_index = 0;
  let results;
  let time = 0.0;
  let length = 0;
  let selectedCategory = "";
  let selectedStartDate = "";
  let selectedEndDate = "";
  let id = "";
  $: {
    selectedQuery = params.query;
    companies = getCompanyResults();
    getResults(selectedQuery, selectedCategory, selectedStartDate, selectedEndDate);
  }
  let width = "50%";
  let padding = "0.6rem";
  let categories = [
    { name: "All", subName: "", selected: true },
    { name: "cybersecurity", subName: "cybersecurity", selected: false },
    { name: "software", subName: "software", selected: false },
    { name: "hardware", subName: "hardware", selected: false },
    { name: "semiconductors", subName: "semiconductors", selected: false },
    { name: "finance", subName: "finance", selected: false },
  ];

  async function getResults(query, category, startDate, endDate) {
    try {
      results = await getQuery(query, category, startDate, endDate);
      time = results.time.toFixed(2)
      length = results.results.docs.length
      searchResults = results.results.docs
      companies = results.company_results
      company = companies[company_index]
      console.log(results);
    } catch (error) {
      console.error('Error fetching query results:', error);
    }
  }

  function selectCategory(category) {
    for (let category_el of categories) {
      category_el.selected = category === category_el;
    }
    categories = [...categories];
    selectedCategory = category.subName;
    console.log(selectedCategory)
  }

  function applyFilter(startDate, endDate) {
    if (endDate <= startDate) {
      alert("End date must be after start date.")
      return
    }
    selectedStartDate = startDate + "T00:00:00Z"
    selectedEndDate = endDate + "T00:00:00Z"
  }

  function resetFilter() {
    selectedStartDate = ""
    selectedEndDate = ""
  }

  function updateCompany(inc) {
    company_index += inc;
    if (company_index < 0) {
      company_index = companies.length - 1;
    } else if (company_index >= companies.length) {
      company_index = 0;
    }
    company = companies[company_index];
  }
</script>

<div class="content">
  <section class="resultsPageSearch">
    <div class="col">
      <div class="row">
        <h2 class="searchLogo" on:click={() => push("/")}>Stocks Guru</h2>
      </div>
      <SearchBar {selectedQuery} {width} {padding} {selectedCategory} {selectedStartDate} {selectedEndDate} />
      <div class="row" style="gap: 0.5rem;">
        {#each categories as category}
          <Category {category} {selectCategory} />
        {/each}
        <DateFilter {applyFilter} {resetFilter} />
      </div>
    </div>
  </section>
  <hr />
  <div class="row" style="gap:10rem; padding-right:3rem;">
    <section class="results">
      <h5 class="time">{length} Results in {time} seconds</h5>
      {#if searchResults.length > 0}
        {#each searchResults as result}
          <Result {result} />
        {/each}
      {:else}
        <p>No results found.</p>
      {/if}
      <div style="margin-bottom: 2rem;"></div>
    </section>
    <section class="companyInfo">
      {#if company}
        <Company {company} {updateCompany} />
      {:else}
        <p>No company found.</p>
      {/if}
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
