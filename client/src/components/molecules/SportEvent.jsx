import React from "react";
import { formatMatchDate } from "@/utils/formatMatchDate";
import { useBets } from "@/context/betsContext";
import BetButton from "@/components/atoms/Bet/BetButton";
import { Link } from "react-router";

const SportEvent = ({ match }) => {
  const { selectedBets, toggleBet } = useBets();
  const selectedBet = selectedBets[match.id];

  return (
    <div className="bg-card rounded-md p-3">
      <p className="text-xs text-gray-700">
        {formatMatchDate(match.start_time)}
      </p>

      <div className="flex justify-between items-center gap-3">
        <Link to={`/match/${match.id}`} className="flex-1">
          <span className="font-bold">{match.home_team}</span>

          <span className="flex flex-col text-sm">
            <span className="font-bold">{match.away_team}</span>
          </span>
        </Link>

        <div className="flex gap-2">
          {match.bet_options
            ?.filter(
              (opt) =>
                opt.bet_type === "1X2" ||
                opt.bet_type === "match_winner"
            )
            .map((opt) => (
              <BetButton
                key={opt.id || opt.value}
                title={opt.value}
                odds={opt.odds}
                isSelected={selectedBet?.value === opt.value}
                onClick={() => toggleBet(match, opt)}
              />
            ))}
        </div>
      </div>
    </div>
  );
};

export default SportEvent;
