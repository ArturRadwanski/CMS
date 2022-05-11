<script>
    import { contentEditMode } from "../stores";
    import New from "./New.svelte";

    export let news = [];
    export let edit;
    export let add;
    export let del;
</script>

<div>
    {#each news as ne, i}
        <New
            title={ne.title}
            text={ne.text}
            medit={edit}
            index={i}
            mdel={del}
        />
    {/each}
    {#if $contentEditMode}
        <button
            on:click={add}
            style="border: none;border-radius: 5px; background-color: var(--primary-background-color);"
            >+</button
        >
    {/if}
</div>
