import { Badge } from "@/components/ui/badge";
import React from "react";

const BetItem = ({ bet, matchId, onRemove }) => {
  return (
    <div className="p-2 rounded">

      {/* MATCH */}
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs">
          {bet.homeTeam} - {bet.awayTeam}
        </span>

        <button
          type="button"
          className="cursor-pointer text-lg"
          onClick={onRemove}
        >
          &#10005;
        </button>
      </div>

      {/* MARKET */}
      <div className="text-xs text-gray-500 mt-2">
        {bet.marketName || bet.betType || "Bet"}
      </div>

      {/* SELECTION + ODDS */}
      <div className="flex justify-between pt-1 text-sm items-center gap-3">
        <div className="font-semibold break-words">
          {bet.betValue || bet.betType || "Selection"}
        </div>

        <Badge className="text-sm shrink-0">
          {bet.odds}
        </Badge>
      </div>

    </div>
  );
};

export default React.memo(BetItem);
