<script>
    import { contentEditMode } from "../stores";
    export let title = "title";
    export let text = "text";
    export let img;
    export let edit;
    export let setImg;
    function abc() {
        edit(
            this.parentElement.children[0].innerText,
            this.parentElement.children[1].innerText
        );
    }
    function changeImg() {
        let inp = document.createElement("input");
        inp.setAttribute("type", "file");
        inp.onchange = () => {
            setImg(inp.files[0]);
        };
        inp.click();
    }
</script>

<div
    style="background-color: var(--primary-background-color); display: inline-block; color: var(--primary-color); border-radius: 10px; overflow: hidden;"
>
    <div style="display: inline-block;">
        <h3 contenteditable={$contentEditMode} on:focusout={abc} style="">
            {title}
        </h3>
        <div contenteditable={$contentEditMode} on:focusout={abc} style="">
            {text}
        </div>
    </div>
    <img
        style="display: inline-block; float: right; max-height: 300px;"
        alt="img"
        src={URL.createObjectURL(img)}
    />
    {#if $contentEditMode}<button on:click={changeImg}>Change Image</button
        >{/if}
</div>
