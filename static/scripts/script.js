document.addEventListener("DOMContentLoaded", function () {
    const images = window.images;

    let currentImageIndex = 0;
    const imageElement = document.getElementById('carousel-image');

    function updateImage() {
      imageElement.src = images[currentImageIndex];
      console.log("Current Image:", images[currentImageIndex]);
    }

    function nextImage() {
      if (currentImageIndex < images.length - 1) {
        currentImageIndex++;
      } else {
        currentImageIndex = 0;
      }
      updateImage();
    }

    function prevImage() {
      if (currentImageIndex > 0) {
        currentImageIndex--;
      } else {
        currentImageIndex = images.length - 1;
      }
      updateImage();
    }

    document.querySelector('.carousel-btn.next').addEventListener('click', nextImage);
    document.querySelector('.carousel-btn.prev').addEventListener('click', prevImage);

    updateImage();
  });