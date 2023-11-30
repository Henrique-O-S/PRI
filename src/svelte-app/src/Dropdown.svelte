<!-- src/Dropdown.svelte -->
<script>
    let selectedQuery = '';
  
    function handleChange(event) {
      selectedQuery = event.target.value;
    }
  
    function handleKeyDown(event) {
      if (event.key === 'Enter') {
        // Call a function or perform an action when Enter is pressed
        performSearch();
      }
    }
  
    function performSearch() {
      // You can perform your search action here
      alert(`Performing search for: ${selectedQuery}`);
    }
  </script>
  
  <section class="section">
    <div class="container">
      <div class="field">
        <label class="label">Enter your query:</label>
        <div class="control">
          <input class="input" type="text" bind:value={selectedQuery} on:input={handleChange} on:keydown={handleKeyDown} placeholder="Search...">
        </div>
      </div>
    </div>
  </section>
  