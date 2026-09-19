import React from "react";
import { formatMatchDate } from "@/utils/formatMatchDate";
import { useBets } from "@/context/betsContext";
import BetButton from "@/components/atoms/BetButton";
import { Link } from "react-router";

const SportEvent = ({ match }) => {
  const { selectedBets, toggleBet } = useBets();
  const selectedBet = selectedBets[match.id];

  return (
    <div className="bg-card rounded-md p-3">
      <p className="text-xs text-gray-700">
        {formatMatchDate(match.start_time)}
      </p>

      <div className="flex justify-between items-center">
        <Link to={`/match/${match.id}`}>
          <span className="font-bold">{match.home_team}</span>
          <span className="flex flex-col">
            <span className="font-bold">{match.away_team}</span>
          </span>
        </Link>

        <div className="flex gap-2">
          {match.bet_options
            ?.filter((opt) => opt.bet_type?.code === "1X2")
            .map((opt) => (
              <BetButton
                key={opt.value}
                title={
                  opt.value === "home"
                    ? "1"
                    : opt.value === "draw"
                    ? "X"
                    : "2"
                }
                odds={opt.odds}
                isSelected={selectedBet?.value === opt.value}
                onClick={() => toggleBet(match, opt)}
              />
            ))}

          {!match.bet_options?.length && (
            <>
              <BetButton
                title="1"
                odds={match.home_win_odds}
                isSelected={false}
                onClick={() => {}}
              />
              <BetButton
                title="X"
                odds={match.draw_odds}
                isSelected={false}
                onClick={() => {}}
              />
              <BetButton
                title="2"
                odds={match.away_win_odds}
                isSelected={false}
                onClick={() => {}}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default SportEvent;
