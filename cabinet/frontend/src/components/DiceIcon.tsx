const PIP_MAPS: Record<number, number[]> = {
  1: [0, 0, 0, 0, 1, 0, 0, 0, 0],
  2: [1, 0, 0, 0, 0, 0, 0, 0, 1],
  3: [1, 0, 0, 0, 1, 0, 0, 0, 1],
  4: [1, 0, 1, 0, 0, 0, 1, 0, 1],
  5: [1, 0, 1, 0, 1, 0, 1, 0, 1],
  6: [1, 0, 1, 1, 0, 1, 1, 0, 1],
};

interface DiceIconProps {
  face: number;
  small?: boolean;
}

export default function DiceIcon({ face, small }: DiceIconProps) {
  const map = PIP_MAPS[face] || PIP_MAPS[1];
  return (
    <div className={`dice-icon${small ? " sm" : ""}`}>
      {map.map((on, i) => (
        <div key={i} className={`dpip${on ? " on" : ""}`} />
      ))}
    </div>
  );
}
