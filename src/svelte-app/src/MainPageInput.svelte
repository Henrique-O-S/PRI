<!-- src/MainPageInput.svelte -->
<script>
  import SearchBar from "./SearchBar.svelte";
  let selectedQuery = "";
  let width = "60%";
</script>

<div class="content">
  <section class="main-page-center-section">
    <div class="col">
      <img src="/img/test.jpg" alt="logo" width="400px" />
      <SearchBar {selectedQuery} {width}/>
    </div>
  </section>
</div>

<style>
  div.col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 3rem;
  }

  .content {
    margin: auto; /* Center the content horizontally */
    width: 100%;
  }
</style>
