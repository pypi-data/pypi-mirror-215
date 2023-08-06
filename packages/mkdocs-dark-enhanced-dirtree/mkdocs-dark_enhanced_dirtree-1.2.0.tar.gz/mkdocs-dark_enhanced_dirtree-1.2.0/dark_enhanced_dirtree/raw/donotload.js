function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function setAElements() {
  let all_a_el = document.getElementsByTagName("a");
  for (var i = 0, len = all_a_el.length; i < len; i++) {
    all_a_el[i].onclick = function (e) {
      let url_str = e.target.href;
      if (url_str.includes(window.location.host)) {
        let last_url_char = url_str[url_str.length - 1];
        if (last_url_char === "/") {
          try {
            // loadPage(url_str);
            // setNavActiveByUrl(url_str);
          } catch (e) {
            console.log(e);
          } finally {
            e.preventDefault();
          }
        } else {
          // filter mp4, mp3, etc.... do nothing
        }
      } else {
        // external URL, do nothing (for now)
      }
    };
  }
}

function loadPage(url) {
  let page_content = document.getElementById("page_content");
  page_content.innerHTML = "";
  var xhr = new XMLHttpRequest(); // create new XMLHttpRequest object
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      let content = xhr.responseText.split(
        '<div id="page_content" class="content">'
      )[1];
      content = content.split('<br id="parse-me-away"/>')[0];
      document.getElementById("page_content").innerHTML = content; // update DOM with response
      hljs.highlightAll();
      // setAElements();
    }
  };
  xhr.open("GET", url, true); // open the request with the GET method
  xhr.send(); // send the request
}

/**
 * LOAD - after images and css
 */
window.addEventListener("load", function (event) {});

/**
 * DOMContentLoaded - before css
 */
document.addEventListener("DOMContentLoaded", (event) => {});

/**
 * ====================================
 * ====================================
 * ====================================
 */
(function () {
  console.log("ready");
});

/*
 {%- block scripts %}
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <script src="{{ 'js/bootstrap.js'|url }}"></script>
  {%- endblock %}
*/

// =============================================================

{% if 'mermaid2' in config['plugins'] %}
<script>
	window.addEventListener("load", async function (event) {
		mermaid.initialize({
			theme: "dark"
		});
	});
</script>
{% endif %}

// =============================================================
