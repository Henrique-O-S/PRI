<!-- src/SearchBar.svelte -->
<script>
  import { onMount } from 'svelte';
  import Dropdown from "./Dropdown.svelte";
  import { push } from "svelte-spa-router";
  export let selectedQuery = "";
  export let width = "";
  export let padding = "";
  let showDropdown = false;

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

  // Function to show dropdown
  function handleFocus() {
    showDropdown = true;
  }

  // Function to hide dropdown
  function handleBlur(event) {
    // Use a timeout to allow click events to process
    setTimeout(() => {
      showDropdown = false;
    }, 50);
  }
</script>

<div class="search" style="width: {width};">
  <div class="control">
    <input
      class="searchInput"
      type="text"
      style="padding: {padding};"
      bind:value={selectedQuery}
      on:input={handleChange}
      on:keydown={handleKeyDown}
      on:focus={handleFocus}
      on:blur={handleBlur}
      placeholder="Search for stock news..."
    />
    {#if showDropdown}
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
	gap: 1rem;
}

button.searchButton {
	padding: 0.5rem 1rem;
	margin-left: 1rem;
	font-size: 1.2rem;
	border-radius: 0.5rem;
	cursor: pointer;
	border-color: darkgray;
}

input.searchInput {
	flex: 1;
	font-size: 1.3rem;
	border-radius: 0.8rem;
	border-color: darkgray;
}
</style>
