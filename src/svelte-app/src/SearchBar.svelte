<!-- src/SearchBar.svelte -->
<script>
  import Dropdown from "./Dropdown.svelte";
  import { push } from "svelte-spa-router";
  export let selectedQuery = "";
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
    push(`/results/${query}`);
  }
</script>

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
  <button class="searchButton" on:click={() => performSearch(selectedQuery)}
    >Search</button>
</div>

<style>
  .control {
    display: flex;
    flex: 1;
  }
  div.search {
	display: flex;
	flex-direction: row;
	justify-content: center;
	width: 60%;
	gap: 1rem;
}

button.searchButton {
	padding: 0.5rem 1rem;
	margin-left: 1rem;
	font-size: 1.2rem;
	border-radius: 0.5rem;
	cursor: pointer;
	border-color: black;
}

input.searchInput {
	flex: 1;
	padding: 1rem;
	font-size: 1.4rem;
	border-radius: 0.8rem;
	border-color: darkgray;
}
</style>
