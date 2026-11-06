(() => {
  const menuButton = document.querySelector("[data-nav-toggle]");
  const sidebar = document.querySelector(".sidebar");

  if (menuButton && sidebar) {
    const closeMenu = () => {
      sidebar.classList.remove("is-open");
      menuButton.setAttribute("aria-expanded", "false");
    };

    menuButton.addEventListener("click", () => {
      const open = sidebar.classList.toggle("is-open");
      menuButton.setAttribute("aria-expanded", String(open));
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });

    sidebar.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });
  }

  document.querySelectorAll("[data-table-search]").forEach((input) => {
    const target = document.getElementById(input.dataset.tableSearch);
    if (!target) return;
    const rows = Array.from(target.querySelectorAll("tbody tr"));
    input.addEventListener("input", () => {
      const query = input.value.trim().toLocaleLowerCase();
      rows.forEach((row) => {
        row.hidden = query !== "" && !row.textContent.toLocaleLowerCase().includes(query);
      });
    });
  });
})();
