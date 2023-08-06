let last_active_nav_el = null;

const green_water = "#3bd5b9";
const green_light = "#46db4b";
const blue_light = "#4652db";
const orange_elettric = "#ffbe00";
const red_elettric = "#ff0000";
const pink_light = "#d53b57";
let colors_autoincrement_index = 0;
const colors = [
  blue_light,
  green_water,
  green_light,
  orange_elettric,
  red_elettric,
  pink_light,
];

function getRandomFromColors() {
  colors_autoincrement_index = colors_autoincrement_index + 1;
  let index = colors_autoincrement_index % colors.length;
  return colors[index];
}

function setNavBorder(sub_nav_node) {
  const li_children = sub_nav_node.closest("li.children");
  const li_section = li_children.previousElementSibling;
  if (li_section.classList.contains("collapsed")) {
    sub_nav_nodelist[i].style.borderLeft =
      "0.5px " + getRandomFromColors() + " solid";
  }
}

function setActive(target) {
  if (last_active_nav_el !== null) {
    last_active_nav_el.classList.toggle("active");
  }
  target.classList.toggle("active");
  last_active_nav_el = target;
}

async function setNavActiveByUrl() {
  let li_mdpages_nodelist = this.document.getElementsByClassName("nav-page");
  for (var i = 1, len = li_mdpages_nodelist.length; i < len; i++) {
    let a_el = li_mdpages_nodelist[i].firstElementChild; // get a inside li
    if (a_el.href === window.location.href) {
      setActive(li_mdpages_nodelist[i]);
      const li_children = li_mdpages_nodelist[i].closest("li.children");
      if (li_children) {
        let li_section = li_children.previousElementSibling;
        while (li_section) {
          if (li_section.classList.contains("section")) {
            li_section.classList.add("collapsed");
            let li_children = li_section.closest("li.children");
            li_section =
              li_children !== null ? li_children.previousElementSibling : null;
            if (li_section !== null) {
              const sub_nav_node = li_section.closest("ul.sub-nav");
              if (sub_nav_node !== null) setNavBorder(sub_nav_node);
            }
          }
        }
      }
    }
  }
}

window.addEventListener("load", async function (event) {
  this.document.getElementById("page_content").style.display = "none";
  await hljs.highlightAll();
  await setNavActiveByUrl();
  this.document.getElementById("page_content").style.display = "block";

  let pages_nodelist = this.document.getElementsByClassName("nav-page");
  for (var i = 0, len = pages_nodelist.length; i < len; i++) {
    pages_nodelist[i].addEventListener(
      "click",
      function (event) {
        let a_el_page = event.target.firstElementChild; // HTMLAnchorElement
        a_el_page.click();
      },
      false
    );
  }

  /* dirtree functionality === css + js */
  let sections_nodelist = this.document.getElementsByClassName("section");
  for (var i = 0, len = sections_nodelist.length; i < len; i++) {
    sections_nodelist[i].addEventListener(
      "click",
      function (event) {
        event.target.classList.toggle("collapsed");
        // set sub nav border
        const li_children = event.target.nextElementSibling;
        const sub_nav_ul = li_children.firstElementChild;
        sub_nav_ul.style.borderLeft =
          "0.5px " + getRandomFromColors() + " solid";
      },
      false
    );
  }
});
