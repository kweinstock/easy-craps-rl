// Generic clickable betting spot: wraps any bet-area markup, adds the
// `has-bet` class + chip badge, and fires `place_bet` for `spotKey` on click.
export default function BetSpot({ spotKey, className, state, fire, selectedChip, children, onClick }) {
  const amount = state?.bets?.[spotKey] || 0;
  const classes = [className, amount > 0 ? "has-bet" : ""].filter(Boolean).join(" ");

  function handleClick() {
    if (onClick) {
      onClick();
      return;
    }
    fire("place_bet", { spot: spotKey, amount: selectedChip || 1 });
  }

  return (
    <div className={classes} data-bet={spotKey} onClick={handleClick}>
      {children}
      <div className="chip-badge">{amount > 0 ? amount : 0}</div>
    </div>
  );
}
