<script>
import { admin } from "../stores"
import DisplayUser from "./DisplayUser.svelte"
    $: users = load()
    
    async function load() {
        let res = await fetch("/loadUsers", {
            method: "POST"
        })
        return res.json()
    }
    function usersRefresh(newUsers){
        users = newUsers
    }
</script>
<table class="users">
<thead>
    <tr><th>Nickname</th><th>Password</th><th>Permissions</th></tr>
</thead>
<tbody id="tb">
{#await users}
    loading users...
{:then users} 
{#each users as user}
<DisplayUser user={user} afterDel={usersRefresh}/>

{/each}
{/await}

</tbody>
</table>