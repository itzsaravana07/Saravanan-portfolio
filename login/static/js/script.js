(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const nav = document.getElementById("nav-links");
  const toggle = document.getElementById("nav-toggle");

  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });
  nav.addEventListener("click", (e) => {
    if (e.target.matches("a")) {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", false);
    }
  });

  // Active section highlighting
  const links = [...nav.querySelectorAll("a")];
  const spy = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting)
          links.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id));
      });
    },
    { rootMargin: "-45% 0px -50% 0px" }
  );
  document.querySelectorAll("main section[id]").forEach((s) => spy.observe(s));

  // Fade-in on scroll
  const items = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add("in");
            io.unobserve(en.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    items.forEach((el) => io.observe(el));
  }

  // Typing effect for the hero role text
  const t = document.getElementById("typed");
  if (t) {
    const words = t.dataset.words.split("|");
    if (reduce) {
      t.textContent = words[0];
    } else {
      let w = 0, c = 0, del = false;
      const tick = () => {
        const word = words[w];
        t.textContent = word.slice(0, c);
        if (!del && c === word.length) { del = true; return setTimeout(tick, 1600); }
        if (del && c === 0) { del = false; w = (w + 1) % words.length; }
        c += del ? -1 : 1;
        setTimeout(tick, del ? 35 : 70);
      };
      tick();
    }
  }

  // After a form error/success, jump to the contact section
  if (document.body.dataset.focus === "contact")
    document.getElementById("contact").scrollIntoView();

  // Placeholder (not yet configured) links do nothing
  document.querySelectorAll("a[aria-disabled='true']").forEach((a) =>
    a.addEventListener("click", (e) => e.preventDefault())
  );
})();
