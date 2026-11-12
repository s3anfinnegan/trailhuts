export type ShelterType = "lean_to" | "bothy" | "emergency";
export type Region = "ROI" | "NI";
export type ShelterStatus = "active" | "unverified" | "closed";

export interface ShelterProperties {
  id: string;
  name: string;
  type: ShelterType;
  county?: string;
  region: Region;
  enclosed?: boolean;
  fireplace?: boolean;
  capacity?: number;
  owner_or_maintainer?: string;
  status: ShelterStatus;
  last_verified?: string;
  access_notes?: string;
  sources: { url: string; label?: string }[];
  photo?: { url: string; credit?: string; license?: string };
  notes?: string;
}

export type ShelterFeature = GeoJSON.Feature<GeoJSON.Point, ShelterProperties>;
export type ShelterFeatureCollection = GeoJSON.FeatureCollection<GeoJSON.Point, ShelterProperties>;

export interface FilterState {
  types: Set<ShelterType>;
  region: Region | "";
  hasPhotoOnly: boolean;
  search: string;
}
