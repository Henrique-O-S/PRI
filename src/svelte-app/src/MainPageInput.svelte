<!-- src/MainPageInput.svelte -->
<script>
  import Dropdown from "./Dropdown.svelte";
  import { push } from "svelte-spa-router";
  let selectedQuery = "";
  let showDropdown = false; // Initialize showDropdown variable

  function handleChange(event) {
    selectedQuery = event.target.value;
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      performSearch(selectedQuery);
    }
  }

  function performSearch(query) {
    selectedQuery = query;
    push(`/results/${selectedQuery}`);
  }
</script>

<div class="content">
  <section class="main-page-center-section">
    <div class="col">
      <img src="/img/test.jpg" alt="gato" width="400px" />
      <div class="search">
        <div class="control">
          <input
            class="searchInput"
            type="text"
            bind:value={selectedQuery}
            on:input={handleChange}
            on:keydown={handleKeyDown}
            placeholder="Search for stock news..."
            on:click={() => (showDropdown = !showDropdown)}
          />
          {#if showDropdown}
            <!-- Call the Dropdown component and pass the required props -->
            <Dropdown {performSearch} {selectedQuery} />
          {/if}
        </div>
        <button
          class="searchButton"
          on:click={() => performSearch(selectedQuery)}>Search</button
        >
      </div>
    </div>
  </section>
</div>

<style>
  .control{
    display: flex;
    flex: 1;
  }
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
