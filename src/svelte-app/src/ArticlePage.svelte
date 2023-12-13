<!-- src/ArticlePage.svelte -->
<script>
  import { push, pop } from "svelte-spa-router";
  import Company from "./Company.svelte";
  import {
    fixArticleText,
    getArticleCompanies,
    convertDateString,
  } from "./general_functions.js";
  import Sugestion from "./Sugestion.svelte";
  export let params = {};
  let companies;
  let company;
  let company_index = 0;
  let results;
  let article_title = "";
  let article_date = "";
  let article_link = "";
  let paragraphs = [];
  let suggestions;
  $: {
    companies = [];
    getArticleAndCompanies(params.id);
    suggestions = ["apple", "microsoft", "google", "amazon", "facebook"];
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

  async function getArticleAndCompanies(id) {
    try {
      results = await getArticleCompanies(id);
      // If there is companies, set
      if (results.docs[0].article_companies)
        companies = results.docs[0].article_companies;
      company = companies[company_index];
      article_title = results.docs[0].article_title;
      article_date = results.docs[0].article_date;
      article_link = results.docs[0].article_link;
      paragraphs = fixArticleText(results.docs[0].article_text);
    } catch (error) {
      console.error("Error fetching query results:", error);
    }
  }

  function searchSuggestion(query) {
    push(`/results/${query}`);
  }
</script>

<div class="content">
  <section class="articlePageTop">
    <div class="col">
      <div class="row">
        <h2 class="backButton" on:click={() => pop()}>&#8592;</h2>
      </div>
      <img src="/img/cnbc.png" alt={"cbnc.logo"} style="width: 7%;"/>
      <h1 class="articleTitle">
        {article_title}
      </h1>
      <div class="row articleDetails">
        <h5 class="date">{convertDateString(article_date)}</h5>
        <a class="learnMore" href={article_link}>Learn more</a>
      </div>
    </div>
  </section>
  <hr />
  <div class="row" style="gap:10rem; padding-right:3rem;">
    <section class="text">
      {#each paragraphs as paragraph}
        <p>{paragraph}</p>
      {/each}
    </section>
    <section class="companyInfo">
      {#if companies.length > 0}
        <Company {company} {updateCompany} />
      {:else}
        <h3>No companies found</h3>
      {/if}
    </section>
  </div>
  <hr style="margin-top: 2rem; margin-bottom:0.5rem;" />
  <div class="textFooter">
    <h3 class="searchSuggestions">Search suggestions:</h3>
    <div class="suggestions-row">
      {#each suggestions as suggestion}
        <Sugestion {suggestion} {searchSuggestion} />
      {/each}
    </div>
  </div>
  <div style="padding-bottom: 3rem;"> </div>
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
  section.articlePageTop {
    margin-bottom: 0.5rem;
  }

  h1.articleTitle {
    font-weight: 700;
    font-size: 2rem;
    color: #333;
    margin-top: 0rem;
  }

  h2.backButton {
    font-weight: 700;
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 0;
    padding-left: 0.5rem;
    text-align: start;
    cursor: pointer;
  }

  section.text {
    text-align: justify;
    font-size: 1.1rem;
    text-indent: 1rem;
    padding-left: 1rem;
    margin-bottom: 0.2rem;
    font-weight: 500;
    margin-top: 2rem;
    width: 60%;
  }

  section.text p {
    line-height: 1.7rem;
  }

  section.companyInfo {
    flex: 1;
  }

  hr {
    margin-bottom: 1rem;
    margin-top: 0rem;
    background-color: silver;
    height: 1.5px;
    opacity: 30%;
  }

  .articleDetails {
    justify-content: space-between;
    margin-left: 1rem;
    margin-right: 1rem;
    align-items: center;
  }

  .articleDetails * {
    margin-bottom: 0;
  }

  .articleDetails .date {
    font-size: 0.9rem;
    opacity: 0.5;
  }

  .articleDetails .learnMore {
    font-size: 1rem;
    cursor: pointer;
    color: rgb(81, 81, 225);
  }

  .textFooter {
    justify-content: center;
    text-align: center;
  }

  .suggestions-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem; /* Adjust the gap between suggestions */
    max-width: 1000px; /* Set a maximum width for the row */
    margin: 0 auto; /* Center the row */
    margin-top: 2rem;
  }

  .searchSuggestions {
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    opacity: 0.8;
  }
</style>
