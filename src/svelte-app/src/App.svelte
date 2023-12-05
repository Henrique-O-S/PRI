<!-- src/App.svelte -->
<script>
  import { Router, Route } from 'svelte-routing';
  import MainPageInput from './MainPageInput.svelte';
  import ResultsPage from './ResultsPage.svelte';

  let selectedQuery = '';

  function handleQueryChange(event) {
    selectedQuery = event.detail || event.target.value;
    // You can perform additional logic here, such as fetching data from the backend
  }
</script>

<Router>
  <Route path="/">
    <MainPageInput on:change={handleQueryChange} {selectedQuery} />
  </Route>

  <Route path="/results/:query" let:params>
    <ResultsPage {selectedQuery} />
  </Route>
</Router>

