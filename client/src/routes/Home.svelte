<script>
    import Block from "../components/Block.svelte";
    import News from "../components/News.svelte";
    import Slider from "../components/Slider.svelte";
    import Style from "../components/Style.svelte";
    import {
        contentEditMode,
        admin,
        stylesEditMode,
        stylesSt,
        burger,
        ord,
    } from "../stores";

    function saveStyles() {
        fetch("/saveStyles", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(
                styles.map((a) => ({
                    sel: a.sel,
                    font: a.font,
                    ord: a.ord,
                    col: a.cp1 + "_" + a.cp2 + "_" + a.cb1 + "_" + a.cb2,
                    bur: a.bur,
                }))
            ),
        });
    }

    function saveContent() {
        content.news = content.news.filter((el) => {
            return el.text != "" || el.text != "";
        });
        fetch("/saveContent", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(content),
        });
        let fd = new FormData();
        fd.append("img", blockImg);
        fetch("/saveBImg", {
            method: "POST",
            body: fd,
        });
    }

    $: content = {
        news: [],
        block: {
            title: "",
            text: "",
        },
    };

    $: blockImg = new Blob();

    $: saveWindow = false;

    $: styles = [
        {
            sel: true,
            cp1: "#da99da",
            cp2: "#ffffff",
            cb1: "#4e57ba",
            cb2: "#2a2d37",
            font: "Helvetica,sans-sherif",
            ord: 0,
        },
        {
            sel: true,
            cp1: "#dadada",
            cp2: "#ffffff",
            cb1: "#4e4e4e",
            cb2: "#2a2a2a",
            font: "Helvetica,sans-sherif",
            ord: 0,
        },
    ];

    function loadContent() {
        fetch("/getContent")
            .then((response) => response.json())
            .then((data) => {
                if (data.success) content = data.content;
                console.log(data);
            });
        fetch("getBImg")
            .then((response) => response.blob())
            .then((data) => {
                blockImg = data;
            });
    }
    loadContent();

    async function loadStyles() {
        let s;
        await fetch("/getStyles")
            .then((response) => response.json())
            .then((data) => {
                s = data.map((a) => {
                    let c = a.col.split("_");
                    return {
                        sel: a.sel,
                        font: a.font,
                        ord: a.ord,
                        cp1: c[0],
                        cp2: c[1],
                        cb1: c[2],
                        cb2: c[3],
                        bur: a.bur,
                    };
                });
            });
        console.log(s);
        if (s == undefined || s.length == 0) {
            s = [
                {
                    sel: true,
                    cp1: "#da99da",
                    cp2: "#ffffff",
                    cb1: "#4e57ba",
                    cb2: "#2a2d37",
                    font: "Helvetica,sans-sherif",
                    ord: 0,
                    bur: false,
                },
                {
                    sel: true,
                    cp1: "#dadada",
                    cp2: "#ffffff",
                    cb1: "#4e4e4e",
                    cb2: "#2a2a2a",
                    font: "Helvetica,sans-sherif",
                    ord: 0,
                    bur: false,
                },
            ];
        }
        styles = s;
        $stylesSt = styles;
        console.log(styles);
        updGS();
    }
    loadStyles();

    function editNew(i, ntitle, ntext) {
        content.news[i].title = ntitle;
        content.news[i].text = ntext;
        content = content;
        console.log(content);
    }
    function addNew() {
        console.log(content);
        let n = { title: "title", text: "text" };
        content.news.push(n);
        content = content;
    }
    function deleteNew(i) {
        content.news.splice(i, 1);
        content = content;
    }
    function editBlock(ntitle, ntext) {
        content.block.title = ntitle;
        content.block.text = ntext;
        content = content;
    }
    function onSaveButton() {
        $contentEditMode = false;
        saveWindow = true;
    }
    function saveConfirm() {
        saveWindow = false;
        saveContent();
    }
    function setImage(file) {
        blockImg = file;
    }
    function setStyle(s, i) {
        if (s.sel) {
            styles = styles.map((a) => {
                let b = a;
                b.sel = false;
                return b;
            });
            s.sel = true;
        }
        styles[i] = s;
        styles = styles;
        $stylesSt = styles;
        console.log(styles);
        updGS();
    }
    function updGS() {
        let cs = styles.find((a) => a.sel);
        if (cs == undefined) cs = styles[0];
        let root = document.documentElement;
        root.style.setProperty("--primary-color", cs.cp1);
        root.style.setProperty("--secondary-color", cs.cp2);
        root.style.setProperty("--primary-background-color", cs.cb1);
        root.style.setProperty("--secondary-background-color", cs.cb2);
        root.style.setProperty("--font", cs.font);
        $ord = cs.ord;
        $burger = cs.bur;
    }
</script>

<h1>Home</h1>
{#if $contentEditMode}<button on:click={onSaveButton}>Exit Edit Mode</button
    >{:else if $stylesEditMode}
    <button
        on:click={() => {
            $stylesEditMode = false;
            saveStyles();
        }}>Exit</button
    ><button
        on:click={() => {
            function downloadObjectAsJson(exportObj, exportName) {
                var dataStr =
                    "data:text/json;charset=utf-8," +
                    encodeURIComponent(JSON.stringify(exportObj));
                var downloadAnchorNode = document.createElement("a");
                downloadAnchorNode.setAttribute("href", dataStr);
                downloadAnchorNode.setAttribute(
                    "download",
                    exportName + ".json"
                );
                document.body.appendChild(downloadAnchorNode); // required for firefox
                downloadAnchorNode.click();
                downloadAnchorNode.remove();
            }
            downloadObjectAsJson(styles, "stylesExport");
        }}>Export To JSON</button
    ><button
        on:click={() => {
            let inp = document.createElement("input");
            inp.setAttribute("type", "file");
            inp.onchange = () => {
                var reader = new window.FileReader();
                reader.onload = (event) => {
                    styles = JSON.parse(event.target.result);
                };
                reader.readAsText(inp.files[0]);
            };
            inp.click();
        }}>Import From JSON</button
    >
{:else if $admin}
    <div class="edit-btns-container">
        <button
            class="login-button"
            on:click={() => {
                $contentEditMode = true;
            }}>Edit Content</button
        ><button
            class="login-button"
            on:click={() => {
                $stylesEditMode = true;
            }}>Edit Styles</button
        >
    </div>
{/if}

<div
    style="display: grid; grid-template-columns: auto; margin: auto; width: 80%; gap: 30px;"
>
    {#if $stylesEditMode}
        {#each styles as style, i}
            <Style styl={style} ind={i} sStyle={setStyle} />
        {/each}
    {:else}
        {#if $ord == 0}
            <Slider />
            <News
                news={content.news}
                edit={editNew}
                add={addNew}
                del={deleteNew}
            />
            <Block
                {...content.block}
                edit={editBlock}
                img={blockImg}
                setImg={setImage}
            />
        {/if}
        {#if $ord == 1}
            <Slider />
            <Block
                {...content.block}
                edit={editBlock}
                img={blockImg}
                setImg={setImage}
            />
            <News
                news={content.news}
                edit={editNew}
                add={addNew}
                del={deleteNew}
            />
        {/if}
        {#if $ord == 2}
            <News
                news={content.news}
                edit={editNew}
                add={addNew}
                del={deleteNew}
            />
            <Slider />
            <Block
                {...content.block}
                edit={editBlock}
                img={blockImg}
                setImg={setImage}
            />
        {/if}
        {#if $ord == 3}
            <News
                news={content.news}
                edit={editNew}
                add={addNew}
                del={deleteNew}
            />
            <Block
                {...content.block}
                edit={editBlock}
                img={blockImg}
                setImg={setImage}
            />
            <Slider />
        {/if}
        {#if $ord == 4}
            <Block
                {...content.block}
                edit={editBlock}
                img={blockImg}
                setImg={setImage}
            />
            <Slider />
            <News
                news={content.news}
                edit={editNew}
                add={addNew}
                del={deleteNew}
            />
        {/if}
        {#if $ord == 5}
            <Block
                {...content.block}
                edit={editBlock}
                img={blockImg}
                setImg={setImage}
            />
            <News
                news={content.news}
                edit={editNew}
                add={addNew}
                del={deleteNew}
            />
            <Slider />
        {/if}
    {/if}
</div>
{#if saveWindow}
    <div
        style="position: absolute; top: 0px; left: 0px; bottom: 0px; right: 0px; background-color: black; opacity: 80%"
    >
        <div
            style="position: relative; margin: auto; background: white; margin-top: 40%;"
        >
            <h5>save changes?</h5>
            <button on:click={saveConfirm}>yes</button><button
                on:click={() => {
                    loadContent();
                    saveWindow = false;
                }}>no</button
            >
        </div>
    </div>
{/if}

<style>
    .edit-btns-container {
        width: 30%;
        margin: auto;
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
</style>
