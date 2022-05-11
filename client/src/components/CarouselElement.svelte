<script>
    import { contentEditMode } from "../stores";
    export let image;
    export let title = "TITLE";
    export let description = "";
    export let active = false;
    export let reLoadSlides;

    function toString(img) {
        let url = "data:image/*;base64," + img;
        return url;
    }
</script>

<div class={active ? "carousel-item active" : "carousel-item"}>
    <img src={toString(image)} class="d-block w-100" alt="" />
    <div class="carousel-caption d-none d-md-block">
        <h5>
            {title}{#if $contentEditMode}
                <button
                    on:click={() => {
                        fetch("/delSlider", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({ title: title }),
                        }).then((response) => {
                            reLoadSlides();
                        });
                    }}>Delete Slide</button
                >{/if}
        </h5>
        <p>{description}</p>
    </div>
</div>

<style>
    img {
        height: 300px;
    }
    h5 {
        color: var(--secondary-color);
        text-shadow: 0 -1px 4px var(--secondary-background-color);
    }
    p {
        text-shadow: 0 -1px 4px var(--secondary-background-color);
    }
</style>
