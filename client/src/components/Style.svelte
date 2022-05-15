<script>
    export let styl;
    export let ind;
    export let sStyle;
    export let delStyle;
    export let dupStyle;
    let bbb = styl.bur ? "1" : "0";
    let fff = styl.font;
    function update() {
        let eles = this.parentElement.children;
        styl.cp1 = eles[0].value;
        styl.cp2 = eles[1].value;
        styl.cb1 = eles[2].value;
        styl.cb2 = eles[3].value;
        styl.font = eles[4].value;
        styl.bur = eles[5].value == 1 ? true : false;
        styl.sel = eles[6].checked;
        sStyle(styl, ind);
    }
    const ma = ["slider", "news", "block"];
    const p1l = "001122";
    const p2l = "120201";
    const p3l = "212010";
    let p1 = "";
    let p2 = "";
    let p3 = "";
    function upvis() {
        let n = styl.ord;
        p1 = ma[Number(p1l[n])];
        p2 = ma[Number(p2l[n])];
        p3 = ma[Number(p3l[n])];
    }
    upvis();
    const swap = ["240513", "103254"];
    function swapOrd(w) {
        styl.ord = Number(swap[w][styl.ord]);
        upvis();
        sStyle(styl, ind);
    }
</script>

<div style="position: relative;">
    <input type="color" value={styl.cp1} on:input={update} />
    <input type="color" value={styl.cp2} on:input={update} />
    <input type="color" value={styl.cb1} on:input={update} />
    <input type="color" value={styl.cb2} on:input={update} />
    <select on:input={update} bind:value={fff}>
        <option value="Helvetica,sans-sherif">Helvetica</option>
        <option value="Impact,Charcoal,sans-sherif">Impact</option>
        <option value="Trebuchet,sans-sherif">Trebuchet</option>
    </select>
    <select on:input={update} bind:value={bbb}>
        <option value="0">Standard Menu</option>
        <option value="1">Burger Menu</option>
    </select>
    <input type="radio" name="sel" on:change={update} checked={styl.sel} />
    <div class="styleordpar">
        <div>{p1}</div>
        <button
            on:click={() => {
                swapOrd(0);
            }}>&#8593;&#8595;</button
        >
        <div>{p2}</div>
        <button
            on:click={() => {
                swapOrd(1);
            }}>&#8593;&#8595;</button
        >
        <div>{p3}</div>
    </div>
    <button
        on:click={() => {
            dupStyle(ind);
        }}>duplicate</button
    >
    <button
        on:click={() => {
            delStyle(ind);
        }}>delete</button
    >
</div>

<style>
    .styleordpar > div {
        width: 40%;
        background-color: white;
        margin: auto;
    }
</style>
