import HomeContent from "@/components/organisms/HomeContent";
import LeftPanel from "@/components/organisms/panels/LeftPanel";
import Navbar from "@/components/organisms/navigation/Navbar";
import RightPanel from "@/components/organisms/panels/RightPanel";
import MobileBetSlip from "@/components/organisms/MobileBetSlip";
import { BetsProvider } from "@/context/betsContext";
import React from "react";

const HomePage = () => {
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

          {/* MAIN CONTENT */}
          <section
            className="
              w-full
              px-3
              sm:px-4
              lg:px-2
              lg:col-span-5
            "
          >
            <HomeContent />
          </section>

          {/* RIGHT PANEL - DESKTOP */}
          <section className="hidden lg:block lg:col-span-2">
            <RightPanel />
          </section>
        </main>

        {/* BETSLIP - MOBILE */}
        <MobileBetSlip />
      </BetsProvider>
    </div>
  );
};

export default HomePage;
