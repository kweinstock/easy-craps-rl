// Mirrors backend/app/engine/constants.py — display data only.
// The backend is the source of truth for actual payouts/resolution.

export const POINT_NUMBERS = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12];

export const POINT_LABEL = {
  2: "2", 3: "3", 4: "4", 5: "5", 6: "SIX",
  8: "8", 9: "NINE", 10: "10", 11: "11", 12: "12",
};

export const PLACE_PAY = {
  2: [13, 2], 3: [15, 4], 4: [14, 5], 5: [12, 5], 6: [13, 6],
  8: [13, 6], 9: [12, 5], 10: [14, 5], 11: [15, 4], 12: [13, 2],
};

export const HARDS = [
  { n: "HARD 6", combo: [3, 3], sum: 6, payFor: 10 },
  { n: "HARD 10", combo: [5, 5], sum: 10, payFor: 8 },
  { n: "HARD 8", combo: [4, 4], sum: 8, payFor: 10 },
  { n: "HARD 4", combo: [2, 2], sum: 4, payFor: 8 },
];

export const HORN = [
  { n: "2", combo: [1, 1], sum: 2, payFor: 31 },
  { n: "3", combo: [1, 2], sum: 3, payFor: 16 },
  { n: "12", combo: [6, 6], sum: 12, payFor: 31 },
  { n: "11", combo: [5, 6], sum: 11, payFor: 16 },
];

export const HOP_COMBOS = (() => {
  const combos = [];
  for (let a = 1; a <= 6; a++) {
    for (let b = a; b <= 6; b++) combos.push([a, b]);
  }
  return combos;
})();

export const CHIP_VALUES = [1, 2, 3, 5, 10, 25, 50, 100];

// Which roll totals (2-12) would resolve `spotKey` as a win right now —
// drives the WIN CONDITION sidebar so it reflects the bets actually on the
// table instead of just flashing the last roll.
export function winningNumbersForSpot(spotKey, point) {
  switch (spotKey) {
    case "pass": return point == null ? [7] : [point];
    case "field": return [2, 3, 4, 9, 10, 11, 12];
    case "lowfield": return [2, 3, 4];
    case "highfield": return [10, 11, 12];
    case "c": return [2, 3, 12];
    case "e": return [11];
    case "ce": return [2, 3, 11, 12];
    case "anycraps": return [2, 3, 12];
    case "seven": return [7];
    case "horn": return [2, 3, 11, 12];
    case "lowrolls": return [2, 3, 4, 5, 6];
    case "highrolls": return [8, 9, 10, 11, 12];
    case "rollemall": return [2, 3, 4, 5, 6, 8, 9, 10, 11, 12];
    default: break;
  }
  if (spotKey.startsWith("place_") || spotKey.startsWith("hard_") || spotKey.startsWith("horn_")) {
    return [Number(spotKey.split("_")[1])];
  }
  if (spotKey.startsWith("hop_")) {
    const digits = spotKey.split("_")[1];
    return [Number(digits[0]) + Number(digits[1])];
  }
  return [];
}
