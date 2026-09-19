export const formatBet = (betOption, matchDetails) => ({
  betOptionId: betOption.id,

  homeTeam: matchDetails.home_team,
  awayTeam: matchDetails.away_team,

  odds: betOption.odds,

  betType:
    betOption.bet_type_name ||
    betOption.bet_type ||
    "Bet",

  betValue:
    betOption.value ||
    betOption.label ||
    "",

  marketName:
    betOption.bet_type_name ||
    betOption.bet_type ||
    "Bet",
});

export const formatBetDate = (dateString) => {
  if (!dateString) return "";

  const date = new Date(dateString);

  if (isNaN(date.getTime())) return dateString;

  return new Intl.DateTimeFormat("en-US", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(date);
};

export const getBadgeStyles = (status) => {
  switch (status) {
    case "won":
      return {
        variant: "default",
        className: "bg-green-500 hover:bg-green-600",
      };

    case "lost":
      return {
        variant: "destructive",
      };

    case "pending":
      return {
        variant: "secondary",
      };

    case "active":
      return {
        variant: "secondary",
      };

    case "canceled":
      return {
        variant: "outline",
      };

    default:
      return {
        variant: "secondary",
      };
  }
};
