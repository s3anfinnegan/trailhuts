export function hideSplash(): void {
  const splash = document.getElementById("splash");
  if (!splash) return;
  splash.classList.add("hidden");
  setTimeout(() => splash.remove(), 350);
}

export function setSplashStatus(text: string): void {
  const status = document.getElementById("splash-status");
  if (status) status.textContent = text;
}
