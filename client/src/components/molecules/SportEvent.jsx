import React from "react";
import { formatMatchDate } from "@/utils/formatMatchDate";
import { useBets } from "@/context/betsContext";
import BetButton from "@/components/atoms/Bet/BetButton";
import { Link } from "react-router";

const SportEvent = ({ match }) => {
  const { selectedBets, toggleBet } = useBets();
  const selectedBet = selectedBets[match.id];

  const betOptions = [
    {
      id: `${match.id}-1`,
      bet_type: "1X2",
      value: "1",
      odds: match.home_win_odds,
    },
    {
      id: `${match.id}-X`,
      bet_type: "1X2",
      value: "X",
      odds: match.draw_odds,
    },
    {
      id: `${match.id}-2`,
      bet_type: "1X2",
      value: "2",
      odds: match.away_win_odds,
    },
  ].filter((option) => option.odds !== null && option.odds !== undefined);

  return (
    <div className="bg-card rounded-md p-3">
      <p className="text-xs text-gray-700">
        {formatMatchDate(match.start_time)}
      </p>

      <div className="flex justify-between items-center gap-3">
        <Link to={`/match/${match.id}`} className="flex-1">
          <div className="flex flex-col">
            <span className="font-bold">{match.home_team}</span>
            <span className="font-bold">{match.away_team}</span>
          </div>
        </Link>

        <div className="flex gap-2">
          {betOptions.map((option) => (
            <BetButton
              key={option.id}
              title={option.value}
              odds={option.odds}
              isSelected={selectedBet?.value === option.value}
              onClick={() => toggleBet(match, option)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default SportEvent;
