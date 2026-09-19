import React from "react";
import { formatMatchDate } from "@/utils/date";
import { useBets } from "@/context/betsContext";
import BetButton from "@/components/atoms/Bet/BetButton";
import { Link } from "react-router";

const SportEvent = ({ match }) => {
  const { selectedBets, toggleBet } = useBets();
  const selectedBet = selectedBets[match.id];

  const odds = [
    {
      value: "home",
      title: "1",
      odds: match.home_win_odds,
    },
    {
      value: "draw",
      title: "X",
      odds: match.draw_odds,
    },
    {
      value: "away",
      title: "2",
      odds: match.away_win_odds,
    },
  ];

  return (
    <div className="bg-card rounded-md p-3">
      <p className="text-xs text-gray-700">
        {formatMatchDate(match.start_time)}
      </p>

      <div className="flex justify-between items-center gap-2">
        <Link to={`/match/${match.id}`}>
          <span className="font-bold">{match.home_team}</span>
          <span className="flex flex-col">
            <span className="font-bold">{match.away_team}</span>
          </span>
        </Link>

        <div className="flex gap-2">
          {odds.map((opt) => (
            <BetButton
              key={opt.value}
              title={opt.title}
              odds={opt.odds ?? "-"}
              isSelected={selectedBet?.value === opt.value}
              onClick={() =>
                toggleBet(match.id, {
                  value: opt.value,
                  odds: opt.odds,
                  match,
                })
              }
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default SportEvent;
