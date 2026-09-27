# Look closer — Web, 50 pts

## Objective
A box on the page says "Nothing to see here." The flag is hidden in the page but not rendered on screen.

## Concepts
- What the browser **displays** is not everything in the page.
- HTML **comments** (`<!-- ... -->`), CSS-hidden elements (`display:none`, white-on-white), and `data-*` attributes never show up visually.
- The **Elements/Inspector** tab shows the *live DOM* — better than View Source for JS-built pages, because the popup here is rendered by JavaScript.

## Steps
1. Right-click the empty box → **Inspect** (opens DevTools on that element).
2. In the **Elements** panel, expand neighbouring nodes.
3. Search the DOM: focus the Elements panel, **Ctrl+F**, type `CTF{`.
4. Look for green `<!-- comments -->` or greyed-out `hidden` / `display:none` nodes.

## Flag
```
CTF{hidden_in_plain_sight}
```

## Takeaway
Never trust rendered output. First move on any web challenge: open DevTools and check
**Elements (DOM), Console, Network, Storage, Sources**. Each hides things differently.
