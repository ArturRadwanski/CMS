<script >
    function addDataToServer(img, title, description, href){     //blob string string string
        let body = new FormData()
        body.append("img", img)
        body.append("title", title)
        body.append("description", description)
        body.append("href", href)
        let res = fetch("/pushSlide", {
            method: "POST",
            body:  body,
        }).then(res => res.json())
        return res
    }
    function validateData(){
        let photo = document.getElementById("photo").files[0]
        let title = document.getElementById("title").value
        let desc = document.getElementById("description").value
        //var reader = new FileReader()
        //reader.readAsDataURL(photo)
        //reader.onload = () => console.log({photo: reader.result, title: title, desc: desc})
        if(photo === undefined || title == "" || desc == ""){
            alert("Please do not leave blank fields")
            return
        }
        console.log(photo)
        addDataToServer(photo, title, desc, "/")
    }
</script>
<input type="file" id="photo"/>
<input type="text" id="title" placeholder="title" />
<input type="text" id="description" placeholder="description" />
<button on:click="{validateData}">save</button>