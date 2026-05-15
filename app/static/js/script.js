const slides = [
  {
    title: "Gestão inteligente da produção"
  },
  {
    title: "Monitoramento climático"
  },
  {
    title: "Controle de serviços rurais"
  },
  {
    title: "Gestão de animais e rebanhos"
  }
];

const videos = document.querySelectorAll(".background");
const title = document.getElementById("heroTitle");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const scrollBtn = document.querySelector(".scroll-button");

let current = 0;

function updateSlide(index) {
  current = (index + slides.length) % slides.length;

  videos.forEach((video, i) => {
    const active = i === current;

    video.classList.toggle("active", active);

    if (active) {
      video.currentTime = 0;
      video.play().catch(() => {});
    } else {
      video.pause();
    }
  });

  title.textContent = slides[current].title;
}

nextBtn.addEventListener("click", () => {
  updateSlide(current + 1);
});

prevBtn.addEventListener("click", () => {
  updateSlide(current - 1);
});

scrollBtn.addEventListener("click", () => {
  updateSlide(current + 1);
});

window.addEventListener("load", () => {
  videos.forEach((video) => {
    video.muted = true;
    video.playsInline = true;
  });

  updateSlide(0);
});