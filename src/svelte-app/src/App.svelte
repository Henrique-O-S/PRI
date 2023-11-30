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
    <h1>Stocks Guru</h1>
  </header>
  
  <Dropdown on:change={handleQueryChange} />
  <Results {selectedQuery} />

  <footer>
    <p>&copy; 2023 G82 @FEUP-PRI</p>
  </footer>
</main>

<style>
  body{
	padding: 0;
	margin: 0;
  }
  main {
    text-align: center;
  }

  header {
    background-color: #333;
    color: white;
    padding: 1rem;
    width: 100%;
    top: 0;
    z-index: 1000; /* Ensures the header stays above other content */
  }

  footer {
    background-color: #333;
    color: white;
    padding: 1rem;
    position: fixed;
    width: 100%;
    bottom: 0;
  }
</style>
