import React, { useState } from "react";
import { useBets } from "@/context/betsContext";
import RightPanel from "@/components/organisms/panels/RightPanel";

const MobileBetSlip = () => {
  const { selectedBets } = useBets();
  const [isOpen, setIsOpen] = useState(false);

  const betsCount = Object.keys(selectedBets).length;

  return (
    <div className="lg:hidden">
      {/* OVERLAY */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-[90]"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* BETSLIP PANEL */}
      <div
        className={`
          fixed
          left-0
          right-0
          bottom-0
          z-[100]
          bg-background
          rounded-t-2xl
          shadow-2xl
          transition-transform
          duration-300
          max-h-[85vh]
          overflow-y-auto
          ${
            isOpen
              ? "translate-y-0"
              : "translate-y-full"
          }
        `}
      >
        <div className="sticky top-0 bg-background z-10 flex items-center justify-between px-4 py-3 border-b">
          <div className="font-bold">
            BetSlip ({betsCount})
          </div>

          <button
            type="button"
            onClick={() => setIsOpen(false)}
            className="text-2xl font-bold px-2"
          >
            ×
          </button>
        </div>

        <div className="p-3">
          <RightPanel />
        </div>
      </div>

      {/* FIXED MOBILE BUTTON */}
      {!isOpen && (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className="
            fixed
            left-4
            right-4
            bottom-4
            z-[80]
            h-[52px]
            rounded-xl
            bg-red-500
            text-white
            font-bold
            shadow-lg
            flex
            items-center
            justify-between
            px-5
          "
        >
          <span>BetSlip</span>

          <span className="bg-white text-red-500 rounded-full min-w-[28px] h-[28px] px-2 flex items-center justify-center">
            {betsCount}
          </span>
        </button>
      )}
    </div>
  );
};

export default MobileBetSlip;
