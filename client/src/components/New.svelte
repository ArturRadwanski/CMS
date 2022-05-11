<script>
    import { contentEditMode } from "../stores";
    export let title = "title";
    export let text = "text";
    export let medit;
    export let index;
    export let mdel;
    function abc() {
        medit(
            index,
            this.parentElement.children[0].innerText,
            this.parentElement.children[1].innerText
        );
    }
</script>

<div class="news card">
    <div class="card-body">
    <h4 contenteditable={$contentEditMode} on:focusout={abc} class="card-title">{title}</h4>
    <div contenteditable={$contentEditMode} on:focusout={abc} class="card-text">{text}</div>
    {#if $contentEditMode}<button on:click={() => mdel(index)}>-</button>{/if}
    </div>
</div>
<style>
.news{
    display: inline-block;
    background-color: var(--primary-background-color);
    border-radius: 5px;
    margin: 10px;
    color: var(--primary-color);
    width: 15%;
    min-height: 70px;
    min-width: 100px;
    transition: transform ease 0.2s;
}
.news:hover{
    transform: scale(1.1);
    box-shadow: 0 0 11px var(--secondary-color);
}
</style>
