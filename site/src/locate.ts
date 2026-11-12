import maplibregl, { Map as MapLibreMap, Marker } from "maplibre-gl";

export function setupLocateMe(map: MapLibreMap): void {
  const button = document.getElementById("locate-me") as HTMLButtonElement;
  let marker: Marker | undefined;

  button.addEventListener("click", () => {
    if (!navigator.geolocation) {
      alert("Geolocation isn't available in this browser.");
      return;
    }

    button.disabled = true;
    navigator.geolocation.getCurrentPosition(
      (position) => {
        button.disabled = false;
        const { latitude, longitude } = position.coords;

        if (!marker) {
          const el = document.createElement("div");
          el.style.width = "14px";
          el.style.height = "14px";
          el.style.borderRadius = "50%";
          el.style.background = "#1a73e8";
          el.style.border = "2px solid #ffffff";
          el.style.boxShadow = "0 0 0 2px rgba(26,115,232,0.4)";
          marker = new maplibregl.Marker({ element: el });
        }
        marker.setLngLat([longitude, latitude]).addTo(map);
        map.flyTo({ center: [longitude, latitude], zoom: 13 });
      },
      () => {
        button.disabled = false;
        alert("Couldn't get your location — check location permissions and try again.");
      },
      { enableHighAccuracy: true, timeout: 10_000 }
    );
  });
}
