(function () {
  var root = document.documentElement;
  root.classList.add("js");

  // Slides fade up as they come into view; the cover plays at once.
  var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  var cover = document.querySelector(".cover");
  if (cover) requestAnimationFrame(function () { cover.classList.add("in"); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    slides.forEach(function (s) { if (s !== cover) { s.classList.add("reveal"); io.observe(s); } });
  }

  // Keep the reader on the same slide when they switch language.
  function currentSlide() {
    var best = null, bestTop = -Infinity, line = window.innerHeight * 0.35;
    slides.forEach(function (s) {
      var top = s.getBoundingClientRect().top;
      if (top <= line && top > bestTop) { bestTop = top; best = s; }
    });
    return best;
  }
  document.querySelectorAll(".chip").forEach(function (a) {
    a.addEventListener("click", function () {
      var s = currentSlide();
      var base = a.getAttribute("href").split("#")[0];
      if (s && s.id !== "s1") a.setAttribute("href", base + "#" + s.id);
      else a.setAttribute("href", base);
    });
  });

  // Keep the chosen language chip in view in the scrolling row on phones.
  var active = document.querySelector(".top .chip[aria-current='page']");
  if (active && active.scrollIntoView) {
    var row = active.parentElement;
    row.scrollLeft = active.offsetLeft - row.clientWidth / 2 + active.clientWidth / 2;
  }
})();
