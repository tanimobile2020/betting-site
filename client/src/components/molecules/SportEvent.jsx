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
  ].filter(
    (option) =>
      option.odds !== null &&
      option.odds !== undefined
  );

  return (
    <div className="bg-card rounded-md p-3 mb-2">

      {/* DATE */}
      <p className="text-xs text-gray-700 mb-2">
        {formatMatchDate(match.start_time)}
      </p>

      <div
        className="
          flex
          flex-col
          gap-3
          sm:flex-row
          sm:items-center
          sm:justify-between
        "
      >

        {/* TEAMS */}
        <Link
          to={`/match/${match.id}`}
          className="min-w-0 sm:flex-1"
        >
          <div className="flex flex-col">
            <span className="font-bold text-sm sm:text-base">
              {match.home_team}
            </span>

            <span className="font-bold text-sm sm:text-base">
              {match.away_team}
            </span>
          </div>
        </Link>

        {/* 1 X 2 */}
        <div
          className="
            grid
            grid-cols-3
            gap-2
            w-full
            sm:w-auto
            sm:flex
          "
        >
          {betOptions.map((option) => (
            <BetButton
              key={option.id}
              title={option.value}
              odds={option.odds}
              isSelected={
                selectedBet?.betOptionId === option.id
              }
              className="w-full sm:w-[90px] lg:w-[105px]"
              onClick={() =>
                toggleBet(
                  match.id,
                  option,
                  match
                )
              }
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default SportEvent;
