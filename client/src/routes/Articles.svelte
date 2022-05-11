<script>
import { navigate } from "svelte-routing";
import Filter from "../components/Filter.svelte";
import NavLink from "../components/NavLink.svelte";
import { admin, articles } from "../stores";
import Article from "./Article.svelte";

function addNewArticle(){
navigate("newArticle", {replace: true})
}

function displayArticles(){
    let res = fetch("/getArticles", {
        method: "POST"
    }).then(res => res.json())
    return res
}
function delArticle(e, title){
    if(!confirm("Are you sure?")){
        e.stopPropagation()
        return
}
    let res = fetch("/delArticle", {
        method: "POST",
        body: JSON.stringify({
            title: title,
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => {
        displayArticles().then(data => articles.set(data))
    })
    e.stopPropagation()
}
function editArticle(e, title, content, category){
    navigate(`/editArticle/${title}/${content}/${category}`)
    e.stopPropagation()
}

function contentPreView(content){
    return content.slice(0, 60) + "..."
}
function goToArticle(title, e){
    navigate("/Articles/" + title.replace(" ", "_"))
}
</script>

<Filter />
<div id="articlesContainer">
        {#each $articles as article}
        <div class="card" on:click="{(e) => goToArticle(article[0], e)}">
            <div class="card-body">
              <h5 class="card-title">{article[0]}</h5>
              <h6 class="card-subtitle mb-2">{article[3]}</h6>
              <p class="card-text">{contentPreView(article[1])}</p>
              {#if $admin}
                <p class="card-link"  on:click="{(e) => delArticle(e, article[0])}">Delete</p>
                <p class="card-link" on:click="{(e) => {editArticle(e, article[0], article[1], article[3])}}">Edit</p>
              {/if}
            </div>
          </div>
        {/each}
        {#if $admin}
        <div class="card add" on:click="{addNewArticle}">
        <div class="plus" ></div>
        </div>
        {/if}
    
</div>
<style>
.card{
    background-color: var(--primary-background-color);
    width: 20%;
    height: 30vh;
    transition: transform 0.2s ease;
    margin-top: 3vh;
    min-width: 190px;
    cursor: default;
}
.card:hover {
  transform: scale(1.1);
  box-shadow: 0 0 11px var(--secondary-color);
}
.card-title{
    color: var(--primary-color);
}
.card-subtitle{
    color: var(--secondary-background-color);
}
.card-link{
    color: var(--primary-color);
    display: inline-block;
    cursor: pointer;
}
#articlesContainer{
    display: flex;
    align-items: flex-start;
    gap: 4%;
    margin-left:2%;
    flex-wrap: wrap;
}
.card-text{
    font-size: 13px;
}
.card > .plus{
    margin: auto;
}
.add{
    cursor: pointer;
}
</style>
    
    
