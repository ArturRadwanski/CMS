<footer>
    <div
        style="background-color: var(--primary-background-color); color: var(--secondary-background-color); font-size: 20px;
        height: 30px;"
    >
        © 2022 Copyright: Artur Radwański & Jakub Salawa
    </div>
</footer>

<style>
    footer {
        position: fixed;
        bottom: 0px;
        left: 0px;
        right: 0px;
        height: fit-content;
        padding: auto;
    }
    footer > div {
        transform: translateY(30px);
        transition: all 0.3s;
    }
    footer:hover > div {
        transform: translateY(0px);
        transition: all 0.3s;
    }
</style>
