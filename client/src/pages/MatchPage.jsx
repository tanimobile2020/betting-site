import LeftPanel from "@/components/organisms/panels/LeftPanel";
import Navbar from "@/components/organisms/navigation/Navbar";
import RightPanel from "@/components/organisms/panels/RightPanel";
import BetButton from "@/components/atoms/Bet/BetButton";
import ErrorMessage from "@/components/atoms/ErrorMessage";
import { BetsProvider, useBets } from "@/context/betsContext";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router";
import { sportsAdapter } from "@/services/api";
import { formatMatchDate } from "@/utils/formatMatchDate";


const MatchContent = ({ matchData }) => {
  const { selectedBets, toggleBet } = useBets();

  const groupedMarkets = useMemo(() => {
    const groups = {};

    const options = matchData?.bet_options || [];

    options.forEach((option) => {
      const marketCode = option.bet_type || "unknown";
      const marketName =
        option.bet_type_name ||
        option.bet_type ||
        "Market";

      if (!groups[marketCode]) {
        groups[marketCode] = {
          code: marketCode,
          name: marketName,
          options: [],
        };
      }

      groups[marketCode].options.push(option);
    });

    return Object.values(groups);
  }, [matchData]);

  const selectedBet = selectedBets[matchData.id];

  return (
    <div className="space-y-4">

      {/* Match header */}
      <div className="bg-card rounded-md p-4">
        <div className="text-xs text-muted-foreground mb-2">
          {matchData.league_name}
        </div>

        <div className="text-sm text-muted-foreground mb-3">
          {formatMatchDate(matchData.start_time)}
        </div>

        <div className="flex items-center justify-between gap-4">
          <div>
            <div className="font-bold text-lg">
              {matchData.home_team}
            </div>

            <div className="font-bold text-lg">
              {matchData.away_team}
            </div>
          </div>

          {matchData.status === "live" && (
            <div className="font-bold">
              {matchData.home_score ?? 0}
              {" : "}
              {matchData.away_score ?? 0}
            </div>
          )}
        </div>
      </div>

      {/* Markets */}
      {groupedMarkets.length > 0 ? (
        groupedMarkets.map((market) => (
          <div
            key={market.code}
            className="bg-card rounded-md overflow-hidden"
          >
            <div className="font-bold px-4 py-3 border-b">
              {market.name}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-2 p-3">
              {market.options.map((option) => {
                const isSelected =
                  selectedBet?.id === option.id;

                return (
                  <BetButton
                    key={option.id}
                    title={option.value}
                    odds={option.odds}
                    isSelected={isSelected}
                    onClick={() =>
                      toggleBet(matchData, option)
                    }
                  />
                );
              })}
            </div>
          </div>
        ))
      ) : (
        <div className="bg-card rounded-md p-4 text-center text-muted-foreground">
          No betting markets available for this match.
        </div>
      )}

    </div>
  );
};


const MatchPage = () => {
  const { matchId } = useParams();

  const [matchData, setMatchData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatchData = async () => {
      try {
        setError(null);

        const response =
          await sportsAdapter.getMatchDetails(matchId);

        if (response.error) {
          throw new Error(response.error);
        }

        setMatchData(response);
      } catch (error) {
        setMatchData(null);

        setError(
          error.message ||
          error ||
          "An error occurred while fetching match data."
        );

        console.error(
          "Error fetching match data:",
          error
        );
      }
    };

    fetchMatchData();
  }, [matchId]);

  return (
    <div className="w-full min-h-screen">
      <Navbar />

      <BetsProvider>
        <main className="min-w-[1024px] min-h-screen w-full pt-[75px] grid grid-cols-8 lg:grid-cols-9">

          <section className="col-span-2 lg:col-span-2">
            <LeftPanel />
          </section>

          <section className="col-span-4 lg:col-span-5 px-4 lg:px-2">

            {error ? (
              <ErrorMessage error={error} />
            ) : matchData ? (
              <MatchContent matchData={matchData} />
            ) : (
              <div className="text-center text-gray-500">
                Loading match data...
              </div>
            )}

          </section>

          <section className="col-span-2 lg:col-span-2">
            <RightPanel />
          </section>

        </main>
      </BetsProvider>
    </div>
  );
};

export default MatchPage;
