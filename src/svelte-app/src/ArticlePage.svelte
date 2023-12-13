<!-- src/ArticlePage.svelte -->
<script>
  import { push, pop } from "svelte-spa-router";
  import Company from "./Company.svelte";
  import { fixArticleText, getArticleCompanies, convertDateString } from "./general_functions.js";
  export let params = {};
  let companies;
  let company;
  let company_index = 0;
  let results;
  let article_title = "";
  let article_date = "";
  let article_link = "";
  let paragraphs = [];
  $: {
    companies = [];
    getArticleAndCompanies(params.id);
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
      console.error('Error fetching query results:', error);
    }
  }
  
</script>

<div class="content">
  <section class="articlePageTop">
    <div class="col">
      <div class="row">
        <h2 class="backButton" on:click={() => pop()}>&#8592;</h2>
      </div>
      <h1 class="articleTitle"><img src="/img/cnbc.png" alt={"cbnc.logo"} />{article_title}</h1>
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
      <div class="textFooter row">
        <a
          style="justify-self: end;"
          class="learnMore"
          on:click={() => {
            let dummy = "works";
            push(`/results/${dummy}`);
          }}>More Like This...</a
        >
      </div>
    </section>
    <section class="companyInfo">
      {#if companies.length > 0}
        <Company {company} {updateCompany} />
      {:else}
        <h3>No companies found</h3>
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
    margin-bottom: 2rem;
    margin-top: 3rem;
    justify-content: end;
  }
</style>
