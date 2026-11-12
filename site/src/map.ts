import maplibregl, { Map as MapLibreMap, Popup } from "maplibre-gl";
import leanToIconUrl from "./icons/lean_to.svg?url";
import bothyIconUrl from "./icons/bothy.svg?url";
import emergencyIconUrl from "./icons/emergency.svg?url";
import type { ShelterFeatureCollection, ShelterType } from "./types";

const ICON_URLS: Record<ShelterType, string> = {
  lean_to: leanToIconUrl,
  bothy: bothyIconUrl,
  emergency: emergencyIconUrl,
};

const TYPE_LABELS: Record<ShelterType, string> = {
  lean_to: "Lean-to",
  bothy: "Bothy",
  emergency: "Emergency shelter",
};

// Ireland (island) bounding box, used as the initial view.
const IRELAND_BOUNDS: [[number, number], [number, number]] = [
  [-10.8, 51.2],
  [-5.2, 55.5],
];

const ESRI_WORLD_IMAGERY_URL =
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";

function loadIcon(map: MapLibreMap, id: string, url: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      if (!map.hasImage(id)) map.addImage(id, img);
      resolve();
    };
    img.onerror = () => reject(new Error(`Failed to load icon: ${url}`));
    img.src = url;
  });
}

export async function createMap(
  containerId: string,
  shelters: ShelterFeatureCollection
): Promise<MapLibreMap> {
  const apiKey = import.meta.env.VITE_PROTOMAPS_API_KEY;
  if (!apiKey) {
    console.warn(
      "VITE_PROTOMAPS_API_KEY is not set — copy site/.env.example to site/.env.local and add a free key from https://protomaps.com/dashboard"
    );
  }

  const map = new maplibregl.Map({
    container: containerId,
    style: `https://api.protomaps.com/styles/v5/light/en.json?key=${apiKey ?? ""}`,
    bounds: IRELAND_BOUNDS,
    fitBoundsOptions: { padding: 24 },
  });

  await new Promise<void>((resolve, reject) => {
    map.once("load", () => resolve());
    map.once("error", (e) => {
      reject(
        new Error(
          `Map failed to load (likely a missing/invalid Protomaps API key — see site/.env.example): ${e.error?.message ?? e}`
        )
      );
    });
  });

  // Base vector style layers, captured now so we can hide them en masse
  // when switching to the Satellite layer.
  const baseLayerIds = map.getStyle().layers?.map((l) => l.id) ?? [];

  map.addSource("esri-satellite", {
    type: "raster",
    tiles: [ESRI_WORLD_IMAGERY_URL],
    tileSize: 256,
    attribution: "Imagery © Esri, Maxar, Earthstar Geographics",
  });
  map.addLayer({
    id: "esri-satellite-layer",
    type: "raster",
    source: "esri-satellite",
    layout: { visibility: "none" },
  });

  await Promise.all(
    (Object.entries(ICON_URLS) as [ShelterType, string][]).map(([type, url]) =>
      loadIcon(map, type, url)
    )
  );

  map.addSource("shelters", { type: "geojson", data: shelters });
  map.addLayer({
    id: "shelter-points",
    type: "symbol",
    source: "shelters",
    layout: {
      "icon-image": ["get", "type"],
      "icon-size": 0.75,
      "icon-allow-overlap": true,
    },
  });

  const popup = new Popup({ closeButton: true, closeOnClick: true, maxWidth: "280px" });

  map.on("click", "shelter-points", (e) => {
    const feature = e.features?.[0];
    if (!feature) return;
    const props = feature.properties as Record<string, unknown>;
    const sources = (() => {
      try {
        return JSON.parse(String(props.sources)) as { url: string; label?: string }[];
      } catch {
        return [];
      }
    })();

    const statusClass = props.status === "unverified" ? "status-unverified" : "";
    const sourcesHtml = sources
      .map((s) => `<a href="${s.url}" target="_blank" rel="noopener">${s.label ?? "source"}</a>`)
      .join(", ");

    popup
      .setLngLat((feature.geometry as GeoJSON.Point).coordinates as [number, number])
      .setHTML(
        `<div class="shelter-popup">
          <h3>${props.name}</h3>
          <p class="meta">${TYPE_LABELS[props.type as ShelterType]} · ${props.county ?? ""} ${
          props.region ? `(${props.region})` : ""
        }</p>
          <p class="meta ${statusClass}">Status: ${props.status}${
          props.last_verified ? ` · verified ${props.last_verified}` : " · not recently verified"
        }</p>
          ${props.access_notes ? `<p class="meta">${props.access_notes}</p>` : ""}
          ${sourcesHtml ? `<p class="meta">Sources: ${sourcesHtml}</p>` : ""}
        </div>`
      )
      .addTo(map);
  });

  map.on("mouseenter", "shelter-points", () => {
    map.getCanvas().style.cursor = "pointer";
  });
  map.on("mouseleave", "shelter-points", () => {
    map.getCanvas().style.cursor = "";
  });

  setupLayerSwitcher(map, baseLayerIds);

  return map;
}

function setupLayerSwitcher(map: MapLibreMap, baseLayerIds: string[]): void {
  const buttons = document.querySelectorAll<HTMLButtonElement>("#layer-switcher .layer-btn");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const layer = button.dataset.layer;
      if (!layer || button.disabled) return;

      buttons.forEach((b) => b.classList.toggle("active", b === button));

      const showSatellite = layer === "satellite";
      map.setLayoutProperty("esri-satellite-layer", "visibility", showSatellite ? "visible" : "none");
      baseLayerIds.forEach((id) => {
        if (map.getLayer(id)) {
          map.setLayoutProperty(id, "visibility", showSatellite ? "none" : "visible");
        }
      });
    });
  });
}
