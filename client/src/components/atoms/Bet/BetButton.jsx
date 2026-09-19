import React from "react";
import { Button } from "@/components/ui/button";

const BetButton = ({
  title,
  odds,
  isSelected,
  onClick,
  className = "",
}) => {
  const handleClick = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (onClick) {
      onClick();
    }
  };

  return (
    <Button
      type="button"
      variant="destructive"
      onClick={handleClick}
      className={`
        relative
        flex
        flex-col
        items-center
        justify-center
        gap-0
        w-full
        min-w-0
        min-h-[46px]
        h-[46px]
        px-2
        py-1
        touch-manipulation
        select-none
        cursor-pointer
        ${isSelected ? "bg-primary" : ""}
        ${className}
      `}
    >
      <span
        className="
          pointer-events-none
          select-none
          font-semibold
          text-xs
          truncate
          w-full
          text-center
        "
        style={{ lineHeight: "1.15" }}
      >
        {title}
      </span>

      <span
        className="
          pointer-events-none
          select-none
          font-bold
          text-sm
          w-full
          text-center
        "
        style={{ lineHeight: "1.15" }}
      >
        {odds}
      </span>
    </Button>
  );
};

export default BetButton;
