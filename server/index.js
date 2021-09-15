function initMap() {
  const usa = { lat: 32.977536985809955, lng: -98.99810518823165 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: usa,
  });
}
