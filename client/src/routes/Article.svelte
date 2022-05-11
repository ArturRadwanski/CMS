<script>
import { onMount } from "svelte";
import { loggedIn, nickname, articles } from "../stores";


    export let title;
    let content;
    $: comments = [];
    let category;
    onMount(() => {
        fetch("/showArticle", {
        method: "POST",
        body: JSON.stringify({
            title: title
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        content = data.content
        comments = JSON.parse(data.comments) 
        category = data.category
    })
    })
    
    function pushComment(){
        let comment = document.getElementById("textAreaExample").value
        document.getElementById("textAreaExample").value = ""
        let res = fetch("/pushComment", {
            method: "POST",
            body: JSON.stringify({
                title: title,
                comment: comment,
                nickname: $nickname
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            comments = data
        })
    }
  function deleteComment(e){
    let val = e.target.getAttribute("data-value")
    let nick = e.target.getAttribute("data-author")
    fetch("/delComment",{
      method: "POST",
      body: JSON.stringify({
      comment:{
          comment: val,
          nickname: nick,
        },
        title: title
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(res => res.json())
    .then(data => {comments = data})
  }
</script>

<article class="blog-post">
    <h2 class="blog-post-title">{title}</h2>
    <p id="p">{content}</p>
</article>
<!--Comment section-->
<section>
    
    <div class="container my-5 py-5">
      <div class="row d-flex justify-content-center">
        <div class="col-md-12 col-lg-10 col-xl-8">
          <div class="card">

            {#each comments as comment, i (i)}
            <div class="card mb-3 comment-card">
                <div class="card-body">
                  <div class="d-flex flex-start">
                    <div class="w-100">
                      <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class=" fw-bold mb-0 nick">
                          {comment.nickname}:
                          <span class="ms-2 comment">{comment.comment}</span>
                        </h6>
                        {#if comment.nickname == $nickname}
                          <div class="login-button" data-value='{comment.comment}' data-author='{comment.nickname}'on:click={deleteComment}>
                            Delete Comment
                          </div>
                        {/if}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            {/each}
            
            {#if $loggedIn}
            <div class="card-footer py-3 border-0">
              <div class="d-flex flex-start w-100">
                <div class="form-outline w-100">
                  <textarea class="form-control" id="textAreaExample" rows="4"></textarea>
                  <label class="form-label" for="textAreaExample">Message</label>
                </div>
              </div>
              <div class="float-end mt-2 pt-1">
                <button type="button" class="login-button" on:click = "{pushComment}">Post comment</button>
              </div>
            </div>
            {:else}
            Login to post comments
            {/if}
          </div>
        </div>
      </div>
    </div>
  </section>

<style>
    p{
        width: 80%;
        margin: auto;
        overflow-wrap: break-word;
    }
    textarea{
        background-color: var(--secondary-background-color);
        color: var(--secondary-color)
    }
    textarea:focus{
        background-color: var(--secondary-background-color);
        color: var(--secondary-color);
    }
    .card{
        background-color: var(--primary-background-color);
        color: var(--secondary-color)
    }
    button{
        border: none;
    }
    .nick{
        color: var(--primary-color);
        overflow-wrap: break-word;
    }
    .comment{
        color: var(--secondary-color);
        overflow-wrap: break-word;
    }
    .comment-card{
        border-bottom: 2px var(--secondary-background-color) solid;
    }
    div{
      overflow-wrap: break-word;
    }
    span{
      overflow-wrap: break-word;
      word-break: break-all;
    }
</style>