<script>
    import { Router, Route } from "svelte-routing";
    import NavLink from "./components/NavLink.svelte";
    import Home from "./routes/Home.svelte";
    import {
        loggedIn,
        admin,
        articles,
        nickname,
        stylesSt,
        burger,
        ord,
    } from "./stores.js";
    import AccessManagment from "./routes/accessManagment.svelte";
    import { onMount } from "svelte";
    import LogInOutBtn from "./components/LogInOutBtn.svelte";
    import AuthorizationForm from "./routes/AuthorizationForm.svelte";
    import RegisterButton from "./components/RegisterButton.svelte";
    import EditSlider from "./routes/EditSlider.svelte";
    import NewArticle from "./routes/NewArticle.svelte";
    import Articles from "./routes/Articles.svelte";
    import Article from "./routes/Article.svelte";
    import Carousel from "./components/Carousel.svelte";
    import BurgerMenu from "svelte-burger-menu";
    import Footer from "./components/Footer.svelte";
import Gallery from "./routes/Gallery.svelte";

    // Used for SSR. A falsy value is ignored by the Router.
    export let url = "";
    onMount(() => {
        let styles = $stylesSt;
        function updGS() {
            let cs = styles.find((a) => a.sel);
            if (cs == undefined) cs = styles[0];
            let root = document.documentElement;
            root.style.setProperty("--primary-color", cs.cp1);
            root.style.setProperty("--secondary-color", cs.cp2);
            root.style.setProperty("--primary-background-color", cs.cb1);
            root.style.setProperty("--secondary-background-color", cs.cb2);
            root.style.setProperty("--font", cs.font);
            $ord = cs.ord;
            $burger = cs.bur;
        }
        async function loadStyles() {
            let s;
            await fetch("/getStyles")
                .then((response) => response.json())
                .then((data) => {
                    s = data.map((a) => {
                        let c = a.col.split("_");
                        return {
                            sel: a.sel,
                            font: a.font,
                            ord: a.ord,
                            cp1: c[0],
                            cp2: c[1],
                            cb1: c[2],
                            cb2: c[3],
                            bur: a.bur,
                        };
                    });
                });
            console.log(s);
            if (s == undefined || s.length == 0) {
                s = [
                    {
                        sel: true,
                        cp1: "#da99da",
                        cp2: "#ffffff",
                        cb1: "#4e57ba",
                        cb2: "#2a2d37",
                        font: "Helvetica,sans-sherif",
                        ord: 0,
                        bur: false,
                    },
                    {
                        sel: true,
                        cp1: "#dadada",
                        cp2: "#ffffff",
                        cb1: "#4e4e4e",
                        cb2: "#2a2a2a",
                        font: "Helvetica,sans-sherif",
                        ord: 0,
                        bur: false,
                    },
                ];
            }
            styles = s;
            $stylesSt = styles;
            console.log(styles);
            updGS();
        }
        loadStyles();
        $stylesSt = styles;
        fetch("/checkLogin", {
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                loggedIn.set(data.logged);
                admin.set(data.admin);
                nickname.set(data.nickname);
            });
        displayArticles().then((data) => articles.set(data));
    });

    function displayArticles() {
        let res = fetch("/getArticles", {
            method: "POST",
        }).then((res) => res.json());
        return res;
    }
    function titleToUrl(title) {
        return "Articles/" + title.replace(" ", "_");
    }
</script>

<Router {url}>
    <nav>
        {#if $burger}
            <BurgerMenu>
                <NavLink to="/">Home</NavLink><br />
                <NavLink to="Articles">Articles</NavLink><br />
                <NavLink to="gallery">Gallery</NavLink><br />
                {#if $loggedIn}
                    {#if $admin}
                        <NavLink to="managePermissions"
                            >Manage Permissions</NavLink
                        ><br />
                        <NavLink to="newSlide">Add Slide</NavLink><br />
                    {:else}
                        <NavLink to="managePermissions">Profile</NavLink><br />
                    {/if}
                {/if}
            </BurgerMenu>
        {:else}
            <NavLink to="/">Home</NavLink>
            <NavLink to="Articles">Articles</NavLink>
            <NavLink to="gallery">Gallery</NavLink>
            {#if $loggedIn}
                {#if $admin}
                    <NavLink to="managePermissions">Manage Permissions</NavLink>
                    <NavLink to="newSlide">Add Slide</NavLink>
                {:else}
                    <NavLink to="managePermissions">Profile</NavLink>
                {/if}
            {/if}
        {/if}
        <div class="push-btns">
            <LogInOutBtn />
            <RegisterButton />
        </div>
    </nav>
    <div>
        <Route path="/" component={Home} />
        <Route path="Articles" component={Articles} />
        <Route path="managePermissions" component={AccessManagment} />
        <Route path="gallery" component={Gallery} />
        {#if !$loggedIn}
            <Route path="login"><AuthorizationForm form="/login" /></Route>
            <Route path="register"><AuthorizationForm form="/register" /></Route
            >
        {/if}
        {#if $admin}
            <Route path="newSlide" component={EditSlider} />
            <Route path="newArticle"
                ><NewArticle updateArts={displayArticles} edit={false} /></Route
            >
            <Route path="editArticle/:title/:content/:category" let:params
                ><NewArticle updateArts={displayArticles} {...params} /></Route
            >
        {/if}

        {#each $articles as article (article[0])}
            <Route path={titleToUrl(article[0])}
                ><Article
                    title={article[0]}
                    content={article[1]}
                    comments={article[2]}
                    category={article[3]}
                /></Route
            >
        {/each}
    </div>
    <Footer />
</Router>
