// Estimation prudente : bornes documentées entre 0,26 ml (Google, refroidissement direct)
// et ~0,5 L (UC Riverside, refroidissement + production électrique) par requête cloud.
// Doit rester synchronisée avec backend/main.py (WATER_LITERS_PER_REQUEST).
export const WATER_LITERS_PER_REQUEST = 0.3

export function formatLiters(value) {
  return value.toFixed(1).replace('.', ',')
}
