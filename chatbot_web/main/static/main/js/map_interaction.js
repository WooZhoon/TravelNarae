document.addEventListener("DOMContentLoaded", () => {
  const svg = document.querySelector("#korea-map svg");
  if (!svg) return;

  const paths = svg.querySelectorAll("path");

  paths.forEach(path => {
    path.addEventListener("mouseenter", () => {
      path.style.fill = "#ff9900";
      path.style.transform = "scale(1.02)";
      path.style.transformOrigin = "center";
    });

    path.addEventListener("mouseleave", () => {
      path.style.fill = "";
      path.style.transform = "";
    });

    path.addEventListener("click", () => {
      alert(`선택한 지역: ${path.getAttribute("title") || path.id}`);
    });
  });
});
