<script>
export let user;
export let afterDel;
import {loggedIn, admin, nickname} from "../stores"

$: edited = false
function handleDelete(e){
        let nick = e.target.value //extract nickname from button value
        let users
        if(nickname == 'admin'){
            alert("You cannot delete head admin")
            return
        }
        if(confirm("Are you sure?")){
            if($nickname == nick){
            fetch("/delUser", {
                method: "POST",
                body: JSON.stringify({nickname: nickname}),
                headers: {"Content-Type": "application/json"}
            }).then(res => res.json())
            .then(data =>{
                loggedIn.set(false)
                admin.set(false)
                afterDel(data)
            })
            fetch("/logOut", {
                    method: "POST"
                }).then(() => navigate("/", {replace: true}))
            }
            else{
                fetch("/delUser", {
                method: "POST",
                body: JSON.stringify({nickname: nickname}),
                headers: {"Content-Type": "application/json"}
            }).then(res => res.json())
            .then(data => afterDel(data))
            }
        }
    }
function handleEdit(e){
    let nickname = e.target.value
    if(nickname == "admin"){
        alert("You cannot edit headAdmin")
        return
    }
    console.log(user)
    edited = true;

}
function handleSave(e){
    let oldNickname = e.target.value
    let nickname = document.getElementById("newName").value
    let password = document.getElementById("password").value
    let access = document.getElementById("access").value
    access = access === undefined ? 0 : access
    fetch("/changeUser", {
        method: "POST",
        body: JSON.stringify({
            nickname: nickname,
            password: password,
            access: access,
            oldNickname: oldNickname
        }),
        header:{
            "Content-Type": "applicaton/json"
        }
    }).then(res => res.json())
    .then(data => afterDel(data))
    edited = false;
}
</script>

{#if edited}
<tr>
    <td><input value={user[0]} type="text" id="newName" /></td>
    <td><input type="password" id="password" /></td>
    {#if $admin}
    <td><select id="access">
        {#if user[2] == 0}
        <option value="1">admin</option>
        <option value="0" selected>user</option>
        {:else}
        <option value="1" selected>admin</option>
        <option value="0">user</option>
       
        {/if}
    </select>
    </td>
    {:else}
    <td id="access" value="0">X</td>
    {/if}
    <td><button value = {user[0]} on:click="{handleSave}">Save</button></td>
</tr>   
{:else}

<tr>
    <td>{user[0]}</td>
    <td>#####</td>
    <td>
        {#if user[2]}
            admin
        {:else}
            user
        {/if}
    </td>
    <td><button id="del-user" on:click="{handleDelete}" value={user[0]}>delete</button></td>
    <td><button id="edit-user" value = "{user[0]}" on:click="{handleEdit}">edit</button></td>
</tr>
{/if}
