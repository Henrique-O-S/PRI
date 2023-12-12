<!-- src/SearchBar.svelte -->
<script>
  import { onMount, onDestroy } from 'svelte';
  import Dropdown from "./Dropdown.svelte";
  import { push } from "svelte-spa-router";
  import { getSuggestions } from './general_functions.js'
  export let selectedQuery = "";
  export let selectedCategory = "";
  export let selectedStartDate = "";
  export let selectedEndDate = "";
  export let width = "";
  export let padding = "";
  let searchInput;
  let dropdown;
  let showDropdown = false;
  let suggestions = [];
  let isEmpty = true;


  async function handleChange(event) {
    selectedQuery = event.target.value;
    isEmpty = selectedQuery === "";

    try {
      suggestions = await getSuggestions(selectedQuery);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      performSearch(selectedQuery);
    }
  }

  function performSearch(query, category="", startDate="", endDate="") {
    push(`/results/${query}`);
  }

  function handleClickOutside(event) {
    if (searchInput && dropdown && !searchInput.contains(event.target) && !dropdown.contains(event.target)) {
      showDropdown = false;
    }
  }

  onMount(() => {
    document.addEventListener('click', handleClickOutside);
  });

  onDestroy(() => {
    document.removeEventListener('click', handleClickOutside);
  });

  function handleFocus() {
    showDropdown = true;
  }
</script>

<div class="search" style="width: {width};">
  <div class="control">
    <input
      bind:this={searchInput}
      class="searchInput"
      type="text"
      style="padding: {padding};"
      bind:value={selectedQuery}
      on:input={handleChange}
      on:keydown={handleKeyDown}
      on:focus={handleFocus}
      placeholder="Search for stock news..."
    />
    {#if showDropdown}
      <div bind:this={dropdown}>
        <Dropdown {isEmpty} {suggestions} {performSearch} {selectedQuery} {selectedCategory} {selectedStartDate} {selectedEndDate} />
      </div>
    {/if}
  </div>
  <button class="searchButton" on:click={() => performSearch(selectedQuery, selectedCategory, selectedStartDate, selectedEndDate)}
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
