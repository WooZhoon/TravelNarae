document.addEventListener("DOMContentLoaded", () => {
  const object = document.getElementById("korea-map");
  if (!object) return;

  object.addEventListener("load", () => {
    const svgDoc = object.contentDocument;
    if (!svgDoc) return;

    const paths = svgDoc.querySelectorAll("path");

    paths.forEach(path => {
      // 호버 시 마우스 포인터 변경 및 색상 강조
      path.addEventListener("mouseenter", () => {
        path.style.fill = "#ff9900";
        path.style.transform = "scale(1.02)";
        path.style.transformOrigin = "center";
      });

      path.addEventListener("mouseleave", () => {
        path.style.fill = "";
        path.style.transform = "";
      });

      // 클릭 시 경고창 (추후 상세 지도 전환 가능)
      path.addEventListener("click", () => {
        alert(`선택한 지역: ${path.id}`);
      });
    });
  });
});
