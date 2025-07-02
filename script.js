// --- Fake News Detector: Custom JS --- //

//  Console check
console.log("✅ script.js loaded");

document.addEventListener("DOMContentLoaded", function () {

  // Smooth Scroll for Navbar Links
  document.querySelectorAll('a.nav-link[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  //  Initialize Carousel with options
  const carousel = document.getElementById("heroCarousel");
carousel.addEventListener("slid.bs.carousel", function () {
  document.querySelectorAll('.carousel-caption h1').forEach(el => {
    el.classList.remove("animate__animated", "animate__fadeInDown");
    void el.offsetWidth; // trigger reflow
    el.classList.add("animate__animated", "animate__fadeInDown");
  });
});

  const heroCarousel = document.querySelector('#heroCarousel');
  if (heroCarousel) {
    new bootstrap.Carousel(heroCarousel, {
      interval: 4000,   // 4 seconds between slides
      ride: 'carousel',
      pause: false,
      wrap: true
    });
  }

  //  Optional: Log Bootstrap Tab switching
  const tabs = document.querySelectorAll('#aboutTabs button[data-bs-toggle="tab"]');
  tabs.forEach(tab => {
    tab.addEventListener("shown.bs.tab", function (event) {
      console.log(`Switched to: ${event.target.id}`);
    });
  });
});


function checkSelectedNews() {
  const select = document.getElementById('sampleSelect');
  const selectedText = select.value;

  if (!selectedText || select.selectedIndex === 0) {
    document.getElementById('result').innerText = "Please select a news headline.";
    return;
  }

  document.getElementById('result').innerText = "Checking...";

  fetch('/api/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: selectedText })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('result').innerText = "Prediction: " + data.result;
    document.getElementById('result').style.color = (data.result === "Fake News") ? "red" : "green";
  })
  .catch(error => {
    console.error("Error:", error);
    document.getElementById('result').innerText = "Error checking news.";
  });
}
