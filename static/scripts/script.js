document.addEventListener("DOMContentLoaded", function () {
  const images = window.images;
  let currentImageIndex = 0;

  const imageElement = document.getElementById("carousel-image");

  function updateImage() {
    imageElement.src = images[currentImageIndex];
  }

  window.nextImage = function () {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    updateImage();
  };

  window.prevImage = function () {
    currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
    updateImage();
  };

  updateImage();
});