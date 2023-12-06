<!-- src/MainPageInput.svelte -->
<script>
  import Dropdown from "./Dropdown.svelte";
  let selectedQuery = "";
  let showDropdown = false; // Initialize showDropdown variable

  function handleChange(event) {
    selectedQuery = event.target.value;
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      performSearch(selectedQuery);
    }
  }

  function performSearch(query) {
    selectedQuery = query;
    window.location.href = `/results/${selectedQuery}`;
  }
</script>

<main>
  <header>
    <h1>Stocks Guru</h1>
  </header>

  <div class="main-container">
    <div class="content">
      <section class="main-page-center-section">
        <div class="row">
          <div class="control">
            <input
              class="input"
              type="text"
              bind:value={selectedQuery}
              on:input={handleChange}
              on:keydown={handleKeyDown}
              placeholder="Search for stock news..."
              on:click={() => (showDropdown = !showDropdown)}
            />
            {#if showDropdown}
              <!-- Call the Dropdown component and pass the required props -->
              <Dropdown {performSearch} {selectedQuery} />
            {/if}
          </div>
          <button on:click={() => performSearch(selectedQuery)}>Search</button>
        </div>
      </section>
    </div>
  </div>

  <footer>
    <p>&copy; 2023 G82 @FEUP-PRI</p>
  </footer>
</main>

<style>


  div.row {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 1rem;
  }

  input {
    padding: 1rem;
    font-size: 1.4rem;
    margin-right: 1rem;
    border-radius: 0.8rem;
  }

  button {
    padding: 0.5rem 1rem;
    font-size: 1.2rem;
    border-radius: 0.5rem;
    cursor: pointer;
  }

  main {
    display: flex;
    text-align: center;
    flex-direction: column;
    height: 100vh; /* Ensure the main container takes the full viewport height */
  }

  header, footer {
    background-color: #333;
    color: white;
    padding: 1rem;
    width: 100%;
    flex-shrink: 0; /* Prevent header and footer from shrinking */
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
