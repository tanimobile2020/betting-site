import React from "react";
import { Button } from "@/components/ui/button";

const BetButton = ({
  title,
  odds,
  isSelected,
  onClick,
  className = "",
}) => {
  return (
    <Button
      variant="destructive"
      onClick={onClick}
      className={`
        flex
        flex-col
        items-center
        justify-center
        gap-0
        h-[42px]
        min-w-0
        px-2
        text-xs
        ${isSelected ? "bg-primary" : ""}
        ${className}
      `}
    >
      <span
        className="font-semibold truncate max-w-full"
        style={{ lineHeight: "1.15" }}
      >
        {title}
      </span>

      <span
        className="font-bold text-sm"
        style={{ lineHeight: "1.15" }}
      >
        {odds}
      </span>
    </Button>
  );
};

export default BetButton;
