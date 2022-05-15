<script>
    import { contentEditMode } from "../stores";
    import { onMount } from "svelte";
    onMount(() => {
        let eles = document.querySelector("footer>div").children;
        fetch("/getFooter")
            .then((response) => response.json())
            .then((data) => {
                eles[0].innerText = data.lf;
                eles[2].innerText = data.rf;
            });
    });
</script>

<footer>
    <div
        style="background-color: var(--primary-background-color); color: var(--secondary-background-color); font-size: 20px;
        height: 30px; overflow: auto;"
    >
        <div contenteditable={$contentEditMode}>a</div>
        <div>© 2022 Copyright: Artur Radwański & Jakub Salawa</div>
        <div contenteditable={$contentEditMode}>b</div>
    </div>
</footer>

<style>
    footer {
        position: fixed;
        bottom: 0px;
        left: 0px;
        right: 0px;
        height: fit-content;
        padding: auto;
    }
    footer > div {
        transform: translateY(30px);
        transition: all 0.3s;
    }
    footer > div > div {
        display: inline-block;
    }
    footer:hover > div {
        transform: translateY(0px);
        transition: all 0.3s;
    }
</style>
