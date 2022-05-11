<script>
  import { Link } from "svelte-routing";

  export let to = "";

  function getProps({ location, href, isPartiallyCurrent, isCurrent }) {
    //const isActive = href === "/" ? isCurrent : isPartiallyCurrent || isCurrent;
    const isActive = isCurrent
    let classes = ""
    if (isActive) {
      return { class: "active" };
    }
    return {};
  }
</script>

<Link to="{to}" getProps="{getProps}">
  <slot />
</Link>
