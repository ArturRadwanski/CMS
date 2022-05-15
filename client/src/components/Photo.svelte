<script>
    import {admin} from "../stores"
    export let name = ""
    export let func
    function deletePhoto(){
        fetch("/deletePhoto", {
            method: "POST",
            body: JSON.stringify({name: name}),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(res => {
            func()
        })
    }
</script>

<div class="box">
    <img src="/photos/{name}" alt="photo" />
    {#if $admin}
    <div class="login-button" on:click="{deletePhoto}">Del</div>
    {/if}
</div>
<style>
    img{
        width: 20vw;
        max-height: 600px;
    }
    .login-button{
        background-color: red;
    }
    .box{
        display: flex;
        flex-direction: column;
    }
</style>