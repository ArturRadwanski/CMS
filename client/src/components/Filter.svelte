<script>
    import { articles } from "../stores";

    function applyFilters(){
        let search = document.getElementById("search").value
        let sort = document.getElementById('select').value

        fetch("/applyFilters", {
            method: "POST",
            body: JSON.stringify({
                search: search,
                sort: sort
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => articles.set(data))
    }
</script>

<div class="container">
    <h2>Find Article</h2>
    <input type="text" id="search" placeholder="search"/>
    <div class="set">
        <p>Sort:</p>
        <select class="form-select form-select-sm" id="select">
            <option value="title" selected>title</option>
            <option value="category">category</option>
        </select>
    </div>
    <div class="login-button" on:click="{applyFilters}">Apply</div>
</div>
<style>
    p{
        color: var(--secondary-color);
        width: 30%;
        text-align: left;
    }
    .container{
        width: 20%;
        margin: auto;
        display: flex;
        flex-direction: column;
        height: 25vh;
        justify-content: space-between;
    }
    select{
        width: 70%;
        height: 30px;
    }
    .set{
        display: flex;
    }
    .login-button{
        background-color: var(--primary-background-color);
    }
</style>