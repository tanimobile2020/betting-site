import React from "react";
import BetValue from "@/components/atoms/Bet/BetValue";

const MatchItem = ({ match }) => {
  return (
    <div className="py-2 border-b last:border-b-0">
      <div className="flex justify-between items-center gap-3">
        <div>
          <span className="font-semibold text-sm">
            {match.home_team} vs {match.away_team}
          </span>

          {match.status === "finished" && (
            <span className="text-lg ml-2">
              ({match.home_score}:{match.away_score})
            </span>
          )}

          <div className="text-muted-foreground text-xs">
            <span className="uppercase font-medium">
              {match.status}
            </span>
          </div>
        </div>

        <div className="flex gap-2">
          <div className="text-center">
            <div className="text-xs">1</div>
            <BetValue className="text-lg">
              {match.home_win_odds ?? "-"}
            </BetValue>
          </div>

          <div className="text-center">
            <div className="text-xs">X</div>
            <BetValue className="text-lg">
              {match.draw_odds ?? "-"}
            </BetValue>
          </div>

          <div className="text-center">
            <div className="text-xs">2</div>
            <BetValue className="text-lg">
              {match.away_win_odds ?? "-"}
            </BetValue>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MatchItem;
