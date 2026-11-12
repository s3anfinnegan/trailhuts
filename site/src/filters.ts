import type { Map as MapLibreMap } from "maplibre-gl";
import type { FilterState, Region, ShelterFeatureCollection, ShelterType } from "./types";

function matches(feature: ShelterFeatureCollection["features"][number], state: FilterState): boolean {
  const props = feature.properties;

  if (state.types.size > 0 && !state.types.has(props.type)) return false;
  if (state.region && props.region !== state.region) return false;
  if (state.hasPhotoOnly && !props.photo) return false;

  if (state.search.trim()) {
    const needle = state.search.trim().toLowerCase();
    const haystack = `${props.name} ${props.county ?? ""}`.toLowerCase();
    if (!haystack.includes(needle)) return false;
  }

  return true;
}

export function setupFilters(
  map: MapLibreMap,
  shelters: ShelterFeatureCollection,
  onFilterChange?: (visibleIds: string[]) => void
): void {
  const state: FilterState = {
    types: new Set<ShelterType>(),
    region: "",
    hasPhotoOnly: false,
    search: "",
  };

  const countValue = document.getElementById("count-value") as HTMLSpanElement;
  const chips = document.querySelectorAll<HTMLButtonElement>("#type-chips .chip");
  const regionSelect = document.getElementById("region-select") as HTMLSelectElement;
  const hasPhotoCheckbox = document.getElementById("has-photo-checkbox") as HTMLInputElement;
  const searchInput = document.getElementById("search-input") as HTMLInputElement;
  const countButton = document.getElementById("count-button") as HTMLButtonElement;

  function apply(): void {
    const visible = shelters.features.filter((f) => matches(f, state));
    const visibleIds = visible.map((f) => f.properties.id);

    map.setFilter("shelter-points", ["in", ["get", "id"], ["literal", visibleIds]]);
    countValue.textContent = String(visible.length);
    onFilterChange?.(visibleIds);
  }

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const type = chip.dataset.type as ShelterType;
      if (state.types.has(type)) {
        state.types.delete(type);
        chip.classList.remove("active");
      } else {
        state.types.add(type);
        chip.classList.add("active");
      }
      apply();
    });
  });

  regionSelect.addEventListener("change", () => {
    state.region = regionSelect.value as Region | "";
    apply();
  });

  hasPhotoCheckbox.addEventListener("change", () => {
    state.hasPhotoOnly = hasPhotoCheckbox.checked;
    apply();
  });

  let searchDebounce: ReturnType<typeof setTimeout> | undefined;
  searchInput.addEventListener("input", () => {
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(() => {
      state.search = searchInput.value;
      apply();
    }, 150);
  });

  countButton.addEventListener("click", () => {
    const visible = shelters.features.filter((f) => matches(f, state));
    if (visible.length === 0) return;

    let minLng = Infinity;
    let minLat = Infinity;
    let maxLng = -Infinity;
    let maxLat = -Infinity;
    for (const f of visible) {
      const [lng, lat] = f.geometry.coordinates;
      minLng = Math.min(minLng, lng);
      maxLng = Math.max(maxLng, lng);
      minLat = Math.min(minLat, lat);
      maxLat = Math.max(maxLat, lat);
    }
    map.fitBounds(
      [
        [minLng, minLat],
        [maxLng, maxLat],
      ],
      { padding: 48, maxZoom: 14 }
    );
  });

  apply();
}
