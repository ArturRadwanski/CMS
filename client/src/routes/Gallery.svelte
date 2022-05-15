<script>
import Photo from "../components/Photo.svelte";
import { admin } from "../stores";

let names = getNames()
function addPhoto(){
    let fileUpload = document.createElement("input")
    fileUpload.setAttribute("type", "file")
    fileUpload.setAttribute("accept", "image/*")
    fileUpload.onchange = () =>{
        let formData = new FormData
        formData.append("img", fileUpload.files[0])
        fetch("/addPhoto", {
            method: "POST",
            body: formData,
        })
        .then(res =>{
            names = getNames()
        })
    }
    fileUpload.click()
    
}

function getNames(){
    let res = fetch("/getPhotosNames", {
        method: "POST",
    }).then(res => res.json())
    return res
}

function changeNamesFromPhoto(){
    names = getNames()
}
console.log(names)

</script>
 <div class="photos">
{#await names then names}
    {#each names.files as name}
        <Photo {name} func={changeNamesFromPhoto}/>
    {/each}
    
{/await}
</div>
 {#if $admin}
<div class="login-button" on:click="{addPhoto}">add photo</div>
 {/if}

 <style>
     .login-button{
        background-color: var(--primary-background-color);
    }
    .photos{
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
 </style>