const galleryItems = document.querySelectorAll(".gallery-item img");
const modal = document.getElementById("gallery-modal");
const modalImg = document.querySelector(".modal-img");

galleryItems.forEach((item) => {
  item.addEventListener("click", () => {
    const imgSrc = item.getAttribute("src");
    modalImg.setAttribute("src", imgSrc);
    const modalBootstrap = new bootstrap.Modal(modal);
    modalBootstrap.show();
  });
});
