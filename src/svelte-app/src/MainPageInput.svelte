<!-- src/MainPageInput.svelte -->
<script>
    import { time_ranges_to_array } from "svelte/internal";
  import Dropdown from "./Dropdown.svelte";
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
    alert(`Searching for ${selectedQuery}...`)
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
        on:click={() => (showDropdown = !showDropdown)}
      />
      {#if showDropdown}
        <!-- Call the Dropdown component and pass the required props -->
        <Dropdown {performSearch} />
      {/if}
    </div>
    <button on:click={() => performSearch(selectedQuery)}>Search</button>
  </div>
</section>

<style>
  section.main-page-center-section {
    position: relative;
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
    border-radius: 0.8rem;
  }

  button {
    padding: 0.5rem 1rem;
    font-size: 1.2rem;
    border-radius: 0.5rem;
    cursor: pointer;
  }
</style>
