<script>
  import Tailwindcss from "./Tailwindcss.svelte";
  import Router from "svelte-spa-router";

  import Footer from "./components/Footer.svelte";
  import Header from "./components/Header.svelte";

  import Contact from "./routes/Contact.svelte";
  import Home from "./routes/Home.svelte";
  import Gallery from "./routes/Gallery.svelte";
  import NotFound from "./routes/NotFound.svelte";
</script>

<Tailwindcss />

<div class="flex flex-col min-h-screen">
  <Header />

  <main>
    <Router
      routes={{
        "/": Home,
        "/contact": Contact,
        "/gallery": Gallery,
        "*": NotFound,
      }}
    />
  </main>

  <Footer />
</div>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
