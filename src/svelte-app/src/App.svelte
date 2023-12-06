<!-- src/App.svelte -->
<script lang="ts">
  import Router from "svelte-spa-router";
  import MainPageInput from "./MainPageInput.svelte";
  import ResultsPage from "./ResultsPage.svelte";
  import NotFoundPage from "./NotFoundPage.svelte";

  let routes = {
    "/": MainPageInput,
    "/results/:query": ResultsPage,
    "*": NotFoundPage,
  };
</script>

<main>
  <header>
    <h1>Stocks Guru</h1>
  </header>
  <div class="main-container">
    <Router {routes} />
  </div>
  <footer>
    <p>&copy; 2023 G82 @FEUP-PRI</p>
  </footer>
</main>

<style>
  main {
    display: flex;
    text-align: center;
    flex-direction: column;
    height: 100vh; /* Ensure the main container takes the full viewport height */
  }

  header,
  footer {
    background-color: #333;
    color: white;
    padding: 1rem;
    width: 100%;
    flex-shrink: 0; /* Prevent header and footer from shrinking */
  }
</style>
