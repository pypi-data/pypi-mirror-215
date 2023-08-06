function updateMaxSvgWidth(mermaid_div) {
  const mermaid_svg = mermaid_div.firstElementChild;
  if (mermaid_svg) {
    console.log(mermaid_svg);
    // svg { width: 600px !important; }
    const svg_width = screen.width - 40;
    mermaid_svg.style.maxWidth = svg_width.toString() + "px";
  } else {
    setTimeout(function () {
      updateMaxSvgWidth(mermaid_div);
    }, 250);
  }
}

/**
 * https://www.fileformat.info/info/unicode/char/search.htm
 */
function loadCopyCodeBtn() {
  var codeblock_index = 0;
  const codeblocks = document.querySelectorAll("pre code");

  // 1. add buttons to every codeblock
  codeblocks.forEach(function (codeblock) {
    codeblock.id = "codeblock" + codeblock_index++;
    let div = document.createElement("div");
    // "&#x1f589; Copy";
    div.innerHTML = '<button type="submit" class="copy-code-btn">Copy</button>';
    div.style = "text-align: right; margin-bottom: 5px;";
    codeblock.parentNode.insertBefore(div, codeblock);
  });

  // 2. add copy functionality to every button
  var clipboard = new ClipboardJS(".copy-code-btn", {
    target: function (trigger) {
      return trigger.parentNode.nextElementSibling;
    },
  });
  clipboard.on("success", function (e) {
    console.info("Action:", e.action);
    console.info("Text:", e.text);
    console.info("Trigger:", e.trigger);
  });

  clipboard.on("error", function (e) {
    console.info("Action:", e.action);
    console.info("Text:", e.text);
    console.info("Trigger:", e.trigger);
  });
}

window.addEventListener("load", async function (event) {
  const mermaid_div = document.getElementsByClassName("mermaid")[0];
  if (mermaid_div) updateMaxSvgWidth(mermaid_div);

  loadCopyCodeBtn();
});
