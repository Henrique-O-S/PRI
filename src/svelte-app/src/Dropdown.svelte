<!-- src/Dropdown.svelte -->
<script>
    let selectedQuery = '';
  
    function handleChange(event) {
      selectedQuery = event.target.value;
    }
  </script>
  
  <section class="section">
    <div class="container">
      <div class="field">
        <label class="label">Enter your query:</label>
        <div class="control">
          <input class="input" type="text" bind:value={selectedQuery} on:input={handleChange} placeholder="Search...">
        </div>
      </div>
    </div>
  </section>
  