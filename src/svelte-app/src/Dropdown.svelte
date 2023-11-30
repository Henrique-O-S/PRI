<!-- src/Dropdown.svelte -->
<script>
  let selectedQuery = '';

  function handleChange(event) {
    selectedQuery = event.target.value;
  }
</script>

<select bind:value={selectedQuery} on:change={handleChange}>
  <option value="query1">Query 1</option>
  <option value="query2">Query 2</option>
  <!-- Add more options as needed -->
</select>
