<script>
    import {loggedIn, admin, nickname} from "../stores"
    import {navigate} from "svelte-routing"

    export let form;


    function handleClick(){
        nickname.set(document.querySelector("[name='nickname']").value)
        fetch('logIn', {
            method: "POST",
            body: JSON.stringify({nickname: document.querySelector("[name='nickname']").value,
                                password: document.querySelector("[name='password']").value,
                            }),
             headers: new Headers({
                "content-type": "application/json"
            })
        })
        .then(res => res.json())
        .then((res)=>{
            loggedIn.set(res.logged)
            admin.set(res.admin)
            if(!res.logged){
                alert("Nickname and password do not match, please try again")
                nickname.set("")
            }
            else
                navigate("/", {replace: true})
                
        })
    }

    function register(){
        let login = document.querySelector("[name='nickname']").value
        let pass = document.querySelector("[name='password'").value
        let passCheck = document.querySelector("[name='password2'").value
        console.log(login, pass, passCheck)
        if(pass == "" || login == "" || passCheck == ""){
            alert("Please, do not leave blank fields")
            return
        }
        if(pass != passCheck){
            alert("Passwords do not match")
            return
        }
        fetch("/register", {
            method : "POST",
            body: JSON.stringify({nickname: login,
                                  password: pass}),
            headers: {'Content-Type': "application/json"}
        }).then(res => res.json())
        .then(data =>{
            if(data.success){
                loggedIn.set(true)
                admin.set(false)
                nickname.set(login)
                navigate("/", {replace: true})
            }
            else {alert(data.message)}
    })
}
</script>
{#if form=="/login"}
<div>
<h1>Log in</h1>
    <input type="text" placeholder="nickname" name="nickname" required/>
    <input type="password" placeholder="password" name="password" required/>
    <button on:click="{handleClick}">Log in</button>
</div>
{:else if form=="/register"}
<div>
    <h1>Register</h1>
        <input type="text" placeholder="nickname" name="nickname" required/>
        <input type="password" placeholder="password" name="password" required/>
        <input type="password" placeholder="repeat password" name="password2" required />
        <button on:click="{register}">Register</button>
    </div>
{/if}