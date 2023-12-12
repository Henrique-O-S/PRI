<!-- src/DateFilter.svelte -->
<script>
  export let company;
  export let updateCompany;
</script>

<div class="col" style="margin-top: 2rem; gap: 2rem;">
  <div class="outer">
    <div class="col">
      <div class="row">
        <a class="companyName" href="https://www.cnbc.com/quotes/{company.company_tag}">{company.company_name} </a>
      </div>
      <span class="companyTag">{company.company_tag}</span>
    </div>
    <hr />
    <span class="companyDescription">{company.company_description.slice(0,450)}...</span>
  </div>
  <div class="row">
    <button on:click={() => updateCompany(-1)}>&#9664; </button>
    <button on:click={() => updateCompany(1)}>&#9654; </button>
  </div>
</div>

<style>
  div.outer {
    background-color: aliceblue;
    border: 1px solid lightgray;
    border-radius: 15px;
    padding: 2rem;
    height: 400px;
  }
  div.col {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  hr {
    margin-bottom: 1rem;
    margin-top: 1rem;
    background-color: silver;
    height: 1.5px;
    opacity: 30%;
  }
  .companyName {
    font-size: 2rem;
    font-weight: 700;
    text-decoration: none;
  }
  .companyTag {
    font-size: 1.5rem;
    font-weight: 500;
    opacity: 0.4;
    font-style: italic;
  }
  .companyDescription {
    font-size: 1.1rem;
    font-weight: 500;
    text-align: start;
  }

  button {
    padding: 0.5rem 1rem;
    margin-left: 1rem;
    font-size: 1.2rem;
    border-radius: 0.5rem;
    cursor: pointer;
    border-color: darkgray;
    background-color: aliceblue;
  }
</style>
