<script>
import { navigate } from "svelte-routing";
import {articles} from "../stores.js"
export let updateArts;
export let title = ""
export let content = ""
export let category = ""
export let edit = true;
    function addNewArticle(){
        let tit = document.getElementById("title").value
        let cont = document.getElementById("content").value
        let cat = document.getElementById("category").value
        if(tit == "" || cont == "" || cat == ""){
            alert("Do not leave blank fields")
            return
        }
        if(!edit){
        let res = fetch("/addArticle", {
            method: "POST",
            body: JSON.stringify({
                title: tit,
                content: cont,
                category: cat
            }),
            headers:{
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            if(!data.success)
                alert(data.err)
            else{
                alert("Successfully created new article")
                navigate("/Articles")
                updateArts().then(data => {
                    articles.set(data)
                    console.log(data)
                })
            }
        })
    }
    else{
        fetch("/editArticle", {
            method: "POST",
            body: JSON.stringify({
                title: tit,
                content: cont,
                category: cat,
                oldTitle: title
            }),
            headers:{
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            if(!data.success)
                alert(data.err)
            else{
                updateArts().then(data => {articles.set(data)
                console.log(data)})
                alert("Successfully edited article")
                navigate("/Articles")
                
            }
        })
    }
    }
</script>

<h2>Add new article</h2>
<div>
    <input type="text" placeholder="title" id="title" value={title}/>
    <textarea placeholder="content" id="content" value={content}></textarea>
    <input type="text" placeholder="category" id="category" value={category}/>
    <div class="login-button" on:click="{addNewArticle}">
    {#if edit}
    Edit article
    {:else}
    Add article
    {/if}
    </div>
</div>

<style>
    h2 + div{
        display: flex;
        flex-direction: column;
    }
    textarea{
        resize: both;
    }
    input + div{
        background-color: var(--primary-background-color);
    }
</style>
