<!-- src/App.svelte -->
<script lang="ts">
  import Router, { push } from "svelte-spa-router";
  import MainPageInput from "./MainPageInput.svelte";
  import ResultsPage from "./ResultsPage.svelte";
  import NotFoundPage from "./NotFoundPage.svelte";

  let routes = {
    "/": MainPageInput,
    "/results/:query": ResultsPage,
    "*": NotFoundPage,
  };
  function redirectToHome() {
    // Use push function to navigate to the home route ("/")
    push("/");
  }
</script>

<main>
  <header>
    <div class="headerContent">
      <h1 on:click={redirectToHome}>Stocks Guru</h1>
    </div>
  </header>
  <div class="main-container">
    <Router {routes} />
  </div>
  <footer>
    <h1>&copy; 2023 G82 @FEUP-PRI</h1>
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
    background-color: #403e3e;
    color: white;
    padding: 1rem;
    width: 100%;
    flex-shrink: 0; /* Prevent header and footer from shrinking */
  }

  header h1 {
    cursor: pointer;
  }

  .headerContent {
    display: flex;
    justify-content: center;
  }

  header *,
  footer * {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 700;
  }
</style>
