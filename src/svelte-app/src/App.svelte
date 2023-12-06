<!-- src/App.svelte -->
<script lang="ts">
  import Router from "svelte-spa-router";
  import MainPageInput from './MainPageInput.svelte';
  import ResultsPage from './ResultsPage.svelte';
  import NotFoundPage from './NotFoundPage.svelte';

  let routes = {
    "/": MainPageInput,
    "/results/:query": ResultsPage,
    "*": NotFoundPage
  };

</script>

<main>
  <Router {routes} />
</main>

