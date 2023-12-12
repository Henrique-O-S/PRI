<!-- src/SearchBar.svelte -->
<script>
  import { onMount, onDestroy } from 'svelte';
  import Dropdown from "./Dropdown.svelte";
  import { push } from "svelte-spa-router";
  export let selectedQuery = "";
  export let width = "";
  export let padding = "";
  let searchInput;
  let dropdown;
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
        <Dropdown {performSearch} {selectedQuery} />
      </div>
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
