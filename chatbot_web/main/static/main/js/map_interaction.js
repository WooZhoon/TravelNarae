document.addEventListener("DOMContentLoaded", () => {
  const paths = document.querySelectorAll(".land");

  paths.forEach(path => {
    path.addEventListener("click", () => {
      const previouslyFocused = document.querySelector(".land.focused");

      // 같은 지역을 다시 클릭하면 포커스 해제 + transform 초기화
      if (previouslyFocused === path) {
        path.classList.remove("focused");
        path.style.transform = "none"; // ✅ transform 초기화
        return;
      }

      // 기존 포커스 제거 + transform 초기화
      if (previouslyFocused) {
        previouslyFocused.classList.remove("focused");
        previouslyFocused.style.transform = "none"; // ✅ 기존 transform 해제
      }

      // 현재 클릭한 지역에 포커스 추가
      path.classList.add("focused");

      // 맨 앞으로 올리기
      path.parentNode.appendChild(path);
    });
  });
});
