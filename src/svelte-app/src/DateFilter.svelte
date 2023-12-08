<!-- src/DateFilter.svelte -->
<script>
  export let applyFilter;
  let startDate = new Date().toISOString().split("T")[0]; // Default to current date
  let endDate = new Date().toISOString().split("T")[0]; // Default to current date
  let showDates = false;
</script>

<div class="col" style="gap: 0rem; flex:1">
  <div class="row">
    {#if showDates}
      <span on:click={() => (showDates = !showDates)}>Filter by date &#9650;</span>
    {:else}
      <span on:click={() => (showDates = !showDates)}>Filter by date &#9660;</span>
    {/if}
  </div>
  {#if showDates}
    <div class="outer">
      <div class="inner">
        <div class="row" style="gap: 1rem;">
          <div class="col">
            <div class="row">
              <label for="startDate">Start Date:</label>
              <input type="date" bind:value={startDate} id="startDate" />
            </div>
            <div class="row">
              <label for="endDate">End Date:</label>
              <input type="date" bind:value={endDate} id="endDate" />
            </div>
          </div>
          <button on:click={applyFilter(startDate, endDate)}
            >Apply Filter</button
          >
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  span {
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
  }
  div.outer {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
    flex-direction: row;
    justify-items: center;
  }
  div.inner {
    justify-self: center;
    background-color: aliceblue;
    padding: 1rem;
    border-radius: 15px;
    border: 1px solid lightgray;
  }
  div.row {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }
  div.col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1rem;
  }
  button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border-radius: 0.5rem;
    cursor: pointer;
    border-color: darkgray;
  }

  input {
    flex: 1;
    font-size: 1rem;
    border-radius: 0.8rem;
    border-color: darkgray;
    margin-left: 0.75rem;
  }
</style>
