<!-- src/App.svelte -->
<script>
  import Dropdown from './Dropdown.svelte';
  import Results from './Results.svelte';

  let selectedQuery = '';

  function handleQueryChange(event) {
    selectedQuery = event.detail || event.target.value;
    // You can perform additional logic here, such as fetching data from the backend
  }
</script>

<main>
  <header>
    <h1>Backend Information Retrieval App</h1>
  </header>
  
  <Dropdown on:change={handleQueryChange} />
  <Results {selectedQuery} />

  <footer>
    <p>&copy; 2023 Your App Name</p>
  </footer>
</main>

<style>
	@import './App.css';
</style>
