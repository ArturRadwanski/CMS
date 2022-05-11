<script>
    import Carousel from "./Carousel.svelte";
    let slides = loadSlides();
    function loadSlides() {
        let res = fetch("/loadSlider", {
            method: "POST",
        }).then((res) => res.json());
        return res;
    }
    function reLoadSlides() {
        slides = loadSlides();
    }
</script>

<div>
    {#await slides then slides}
        <Carousel {slides} {reLoadSlides} />
    {/await}
</div>
