<script>
    import CarouselElement from "./CarouselElement.svelte";
    export let slides; //Array<{image: Blob, title: string, description: string}>
    export let reLoadSlides;
</script>

<div
    id="carouselExampleIndicators"
    class="carousel slide"
    data-bs-ride="carousel"
>
    <div class="carousel-indicators">
        {#each slides as slide, i}
            <button
                type="button"
                data-bs-target="#carouselExampleIndicators"
                data-bs-slide-to={i}
                class={i == 0 ? "active" : ""}
                aria-current={i == 0 ? "true" : "false"}
                aria-label="Slide {i + 1}"
            />
            <!--Pierwszy slide aktywny-->
        {/each}
    </div>
    <div class="carousel-inner">
        {#each slides as slide, i}
            <CarouselElement
                {...slide}
                active={i == 0 ? true : false}
                {reLoadSlides}
            />
        {/each}
    </div>
    <button
        class="carousel-control-prev"
        type="button"
        data-bs-target="#carouselExampleIndicators"
        data-bs-slide="prev"
    >
        <span class="carousel-control-prev-icon" aria-hidden="true" />
        <span class="visually-hidden">Previous</span>
    </button>
    <button
        class="carousel-control-next"
        type="button"
        data-bs-target="#carouselExampleIndicators"
        data-bs-slide="next"
    >
        <span class="carousel-control-next-icon" aria-hidden="true" />
        <span class="visually-hidden">Next</span>
    </button>
</div>

<style>
    #carouselExampleIndicators {
        width: 50%;
        margin: auto;
    }
</style>
