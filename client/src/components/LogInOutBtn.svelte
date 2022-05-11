<script>
    import {loggedIn, admin, nickname} from "../stores"
    import {navigate} from "svelte-routing"

    function handleLogin(){
        navigate("/login", {replace: true})
    }
    function handleLogout(){
        loggedIn.set(false)
        admin.set(false)
        nickname.set("")
        fetch("/logOut", {
            method: "POST"
        }).then(() => navigate("/", {replace: true}))
        
    }
</script>

{#if $loggedIn}
    <div on:click="{handleLogout}" class="login-button">Log out</div>
{:else}    
    <div on:click="{handleLogin}" class="login-button">Log in</div>
{/if}