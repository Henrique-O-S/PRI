<!-- src/DateFilter.svelte -->
<script>
  export let company;
  export let updateCompany;
  let expanded = false;
</script>

<div class="col" style="margin-top: 2rem; gap: 2rem;">
  <div class="outer">
    <div class="col">
      <div class="row" style="justify-content: center;">
        <a
          class="companyName"
          href="https://www.cnbc.com/quotes/{company.company_tag}"
        >{company.company_name}</a>
      </div>
      <span class="companyTag">{company.company_tag}</span>
    </div>
    <hr />
    <span class="companyDescription" class:expanded>
      {company.company_description}
    </span>
    {#if company.company_description.length > 450}
      <div class="row" style="justify-content: center;">
        <h6 on:click={() => (expanded = !expanded)}>
          {expanded ? "Read less ▲" : "Read more ▼"}
        </h6>
      </div>
    {/if}
  </div>
  <div class="row" style="justify-content: center;">
    <button on:click={() => updateCompany(-1)}>&#9664;</button>
    <button on:click={() => updateCompany(1)}>&#9654;</button>
  </div>
</div>

<style>
  div.outer {
    background-color: aliceblue;
    border: 1px solid lightgray;
    border-radius: 15px;
    padding: 2rem;
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
    text-align: center;
    display: flex;
    overflow: hidden; /* Prevents overflow */
    max-height: 455px; /* Set your desired max height */
    transition: max-height 0.3s ease; /* Smooth transition for height change */
  }

  .companyDescription.expanded {
    max-height: none; /* Expands the description when expanded */
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

  h6 {
    margin-top: 1.5rem;
    font-size: 1.2rem;
    font-weight: 500;
    text-align: center;
    cursor: pointer;
    width: fit-content;
  }

  .row {
    display: flex;
    flex-direction: row;
  }

  /* Media query for smaller screens */
  @media screen and (max-width: 768px) {
    .companyDescription {
      max-height: 80px; /* Adjust the max height for smaller screens */
    }
  }
</style>
