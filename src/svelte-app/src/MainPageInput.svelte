<!-- src/MainPageInput.svelte -->
<script>
  let selectedQuery = "";

  function handleChange(event) {
    selectedQuery = event.target.value;
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      // Call a function or perform an action when Enter is pressed
      performSearch();
    }
  }

  function performSearch() {
    // You can perform your search action here
    alert(`Performing search for: ${selectedQuery}`);
  }
</script>

<section class="main-page-center-section">
  <div class="row">
    <div class="control">
      <input
        class="input"
        type="text"
        bind:value={selectedQuery}
        on:input={handleChange}
        on:keydown={handleKeyDown}
        placeholder="Search for stock news..."
      />
    </div>
    <button on:click={performSearch}>Search</button>
  </div>
</section>

<style>
  section.main-page-center-section {
    
  }

  div.row {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 1rem;
  }

  input {
    padding: 1rem;
    font-size: 1.4rem;
    margin-right: 1rem;
    /* make it more rounded  */
    border-radius: 0.8rem;
    border-color: black;
  }

  button {
    padding: 0.5rem 1rem;
    font-size: 1.2rem;
    border-radius: 0.5rem;
    border-color: black;
    cursor: pointer;
  }
</style>
