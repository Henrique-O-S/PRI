<!-- src/MainPageInput.svelte -->
<script>
  import SearchBar from "./SearchBar.svelte";
  let selectedQuery = "";
  let width = "60%";
  let padding = "1rem";
</script>

<div class="content">
  <section class="main-page-center-section">
    <div class="col">
      <img src="/img/gurulogo.jpg" alt="logo" width="300px" />
      <h1>Stocks Guru</h1>
      <SearchBar {selectedQuery} {width} {padding}/>
    </div>
  </section>
</div>

<style>
  div.col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
  }

  div.col h1{
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
  }

  .content {
    margin: auto; /* Center the content horizontally */
    width: 100%;
    padding-bottom: 15rem;
  }
</style>
