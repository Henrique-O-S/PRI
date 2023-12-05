<!-- src/App.svelte -->
<script>
  import MainPageInput from './MainPageInput.svelte';
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

  <div class="main-container">
    <div class="content">
      <MainPageInput on:change={handleQueryChange} />
    </div>
  </div>

  <footer>
    <p>&copy; 2023 G82 @FEUP-PRI</p>
  </footer>
</main>

<style>
  body {
    padding: 0;
    margin: 0;
  }

  main {
    display: flex;
    flex-direction: column;
    height: 100vh; /* Ensure the main container takes the full viewport height */
  }

  header, footer {
    background-color: #333;
    color: white;
    padding: 1rem;
    width: 100%;
    flex-shrink: 0; /* Prevent header and footer from shrinking */
    text-align: center;
  }

  .main-container {
    display: flex;
    flex: 1; /* Allow the main container to take up remaining vertical space */
    overflow-y: auto; /* Enable vertical scrolling for the main container content */
  }

  .content {
    text-align: center;
    margin: auto; /* Center the content horizontally */
    width: 100%;
  }
</style>
