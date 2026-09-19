import { sportsAdapter } from "@/services/api";
import { formatBet } from "@/utils/formatBet";
import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

const BetsContext = createContext();

const STORAGE_KEY = "selectedBets";

export const BetsProvider = ({ children }) => {
  const [selectedBets, setSelectedBets] = useState(() => {
    try {
      const storedBets = localStorage.getItem(STORAGE_KEY);

      if (storedBets) {
        return JSON.parse(storedBets);
      }

      return {};
    } catch (error) {
      console.error(
        "Error loading bets from localStorage",
        error
      );

      return {};
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(selectedBets)
      );
    } catch (error) {
      console.error(
        "Error saving bets to localStorage",
        error
      );
    }
  }, [selectedBets]);

  useEffect(() => {
    const validateBets = async () => {
      const matchIds = Object.keys(selectedBets);

      if (matchIds.length === 0) {
        return;
      }

      try {
        const availableMatches =
          await sportsAdapter.validateBetsAvailability({
            matchIds,
          });

        const availableMatchIds = new Set(
          availableMatches.map((match) =>
            match.id.toString()
          )
        );

        setSelectedBets((prev) => {
          const updated = {};

          Object.entries(prev).forEach(
            ([matchId, bet]) => {
              if (availableMatchIds.has(matchId.toString())) {
                updated[matchId] = bet;
              }
            }
          );

          return updated;
        });
      } catch (error) {
        console.error(
          "Error validating bets",
          error
        );
      }
    };

    validateBets();
  }, []);

  const clearBets = () => {
    setSelectedBets({});
  };

  const removeBet = (matchId) => {
    setSelectedBets((prev) => {
      const updated = { ...prev };

      delete updated[matchId];

      return updated;
    });
  };

  const toggleBet = (
    matchId,
    betOption,
    matchDetails
  ) => {
    if (
      !matchId ||
      !betOption ||
      !matchDetails
    ) {
      return;
    }

    setSelectedBets((prev) => {
      const existingBet = prev[matchId];

      /*
       * Clicking the same selection again
       * removes it from the BetSlip.
       */
      if (
        existingBet &&
        String(existingBet.betOptionId) ===
          String(betOption.id)
      ) {
        const updated = { ...prev };

        delete updated[matchId];

        return updated;
      }

      /*
       * A match can have one active selection.
       * Choosing another market/selection replaces
       * the previous selection for that match.
       */
      return {
        ...prev,

        [matchId]: formatBet(
          betOption,
          matchDetails
        ),
      };
    });
  };

  const context = {
    selectedBets,
    clearBets,
    toggleBet,
    removeBet,
  };

  return (
    <BetsContext.Provider value={context}>
      {children}
    </BetsContext.Provider>
  );
};

export const useBets = () =>
  useContext(BetsContext);
