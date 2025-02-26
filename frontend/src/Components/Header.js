import React, { useState, useEffect } from "react";
import "../css/Header.css";
import logoIcon from "../logo.svg";

const Header = () => {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className="header"
      style={{ transform: `translateY(${-Math.min(scrollY, 120)}px)` }}
    >
      <div className="header-content">
        <img src={logoIcon} alt="Coffee Shop Icon" className="logo-icon" />
        <h1 className="logo">Coffee Shop</h1>
      </div>
    </header>
  );
};

export default Header;
