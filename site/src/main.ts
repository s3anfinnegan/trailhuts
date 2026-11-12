import "maplibre-gl/dist/maplibre-gl.css";
import "./styles.css";
import { createMap } from "./map";
import { setupFilters } from "./filters";
import { setupLocateMe } from "./locate";
import { hideSplash, setSplashStatus } from "./splash";
import type { ShelterFeatureCollection } from "./types";

async function main(): Promise<void> {
  setSplashStatus("Loading shelters…");
  const response = await fetch("/data/shelters.geojson");
  if (!response.ok) {
    setSplashStatus("Couldn't load shelter data — try refreshing.");
    return;
  }
  const shelters: ShelterFeatureCollection = await response.json();

  setSplashStatus("Loading map…");
  const map = await createMap("map", shelters);

  setupFilters(map, shelters);
  setupLocateMe(map);

  hideSplash();
}

main().catch((err) => {
  console.error(err);
  setSplashStatus("Something went wrong loading the map.");
});
