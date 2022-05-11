<script>
    import {loggedIn, admin} from "../stores"
    import {navigate} from "svelte-routing"

    function handleClick(){
        navigate("/register", {replace: true})
    }
</script>

{#if !$loggedIn}
    <div on:click="{handleClick}" class="login-button">Register</div>
{/if}