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

 
  //  Optional: Log Bootstrap Tab switching
  const tabs = document.querySelectorAll('#aboutTabs button[data-bs-toggle="tab"]');
  tabs.forEach(tab => {
    tab.addEventListener("shown.bs.tab", function (event) {
      console.log(`Switched to: ${event.target.id}`);
    });
  });
});



