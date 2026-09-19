import LeftPanel from "@/components/organisms/panels/LeftPanel";
import Navbar from "@/components/organisms/navigation/Navbar";
import RightPanel from "@/components/organisms/panels/RightPanel";
import MobileBetSlip from "@/components/organisms/MobileBetSlip";
import BetButton from "@/components/atoms/Bet/BetButton";
import ErrorMessage from "@/components/atoms/ErrorMessage";
import { BetsProvider, useBets } from "@/context/betsContext";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router";
import { sportsAdapter } from "@/services/api";
import { formatMatchDate } from "@/utils/formatMatchDate";

const MatchContent = ({ matchData }) => {
  const { selectedBets, toggleBet } = useBets();

  const [openMarkets, setOpenMarkets] = useState({});

  const groupedMarkets = useMemo(() => {
    const groups = {};

    const options = matchData?.bet_options || [];

    options.forEach((option) => {
      const marketCode =
        option.bet_type || "unknown";

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

  const selectedBet =
    selectedBets[matchData.id];

  const toggleMarket = (marketCode) => {
    setOpenMarkets((prev) => ({
      ...prev,
      [marketCode]: !prev[marketCode],
    }));
  };

  return (
    <div className="space-y-2 pb-4">

      {/* MATCH HEADER */}
      <div className="bg-card rounded-md p-3">
        <div className="text-xs text-muted-foreground mb-1">
          {matchData.league_name}
        </div>

        <div className="text-xs text-muted-foreground mb-2">
          {formatMatchDate(matchData.start_time)}
        </div>

        <div className="flex items-center justify-between gap-3">
          <div className="min-w-0">
            <div className="font-bold text-base break-words">
              {matchData.home_team}
            </div>

            <div className="font-bold text-base break-words">
              {matchData.away_team}
            </div>
          </div>

          {matchData.status === "live" && (
            <div className="font-bold whitespace-nowrap">
              {matchData.home_score ?? 0}
              {" : "}
              {matchData.away_score ?? 0}
            </div>
          )}
        </div>
      </div>

      {/* MARKETS */}
      {groupedMarkets.length > 0 ? (
        groupedMarkets.map((market) => {
          const isOpen =
            !!openMarkets[market.code];

          return (
            <div
              key={market.code}
              className="bg-card rounded-md overflow-hidden"
            >

              {/* MARKET HEADER */}
              <button
                type="button"
                onClick={() =>
                  toggleMarket(market.code)
                }
                className="
                  w-full
                  flex
                  items-center
                  justify-between
                  gap-3
                  px-3
                  py-3
                  text-left
                  border-b
                "
              >
                <div className="min-w-0">
                  <div className="font-bold text-sm">
                    {market.name}
                  </div>

                  <div className="text-[11px] text-muted-foreground mt-0.5">
                    {market.options.length} options
                  </div>
                </div>

                <span
                  className={`
                    text-lg
                    shrink-0
                    transition-transform
                    duration-200
                    ${
                      isOpen
                        ? "rotate-180"
                        : ""
                    }
                  `}
                >
                  ▼
                </span>
              </button>

              {/* MARKET OPTIONS */}
              {isOpen && (
                <div
                  className="
                    grid
                    grid-cols-2
                    sm:grid-cols-3
                    gap-2
                    p-3
                  "
                >
                  {market.options.map(
                    (option) => {
                      const isSelected =
                        String(
                          selectedBet?.betOptionId
                        ) ===
                        String(option.id);

                      return (
                        <BetButton
                          key={option.id}
                          title={option.value}
                          odds={option.odds}
                          isSelected={
                            isSelected
                          }
                          className="w-full"
                          onClick={() =>
                            toggleBet(
                              matchData.id,
                              option,
                              matchData
                            )
                          }
                        />
                      );
                    }
                  )}
                </div>
              )}
            </div>
          );
        })
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

  const [matchData, setMatchData] =
    useState(null);

  const [error, setError] =
    useState(null);

  useEffect(() => {
    const fetchMatchData = async () => {
      try {
        setError(null);

        const response =
          await sportsAdapter.getMatchDetails(
            matchId
          );

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
        <main
          className="
            w-full
            min-h-screen
            pt-[75px]
            pb-[80px]
            lg:pb-0
            lg:grid
            lg:grid-cols-9
          "
        >

          {/* LEFT PANEL - DESKTOP */}
          <section className="hidden lg:block lg:col-span-2">
            <LeftPanel />
          </section>

          {/* MATCH CONTENT */}
          <section
            className="
              w-full
              px-3
              sm:px-4
              lg:px-2
              lg:col-span-5
            "
          >
            {error ? (
              <ErrorMessage error={error} />
            ) : matchData ? (
              <MatchContent
                matchData={matchData}
              />
            ) : (
              <div className="text-center text-gray-500 py-6">
                Loading match data...
              </div>
            )}
          </section>

          {/* RIGHT PANEL - DESKTOP */}
          <section className="hidden lg:block lg:col-span-2">
            <RightPanel />
          </section>
        </main>

        {/* MOBILE BETSLIP */}
        <MobileBetSlip />

      </BetsProvider>
    </div>
  );
};

export default MatchPage;
